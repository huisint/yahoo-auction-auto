# Copyright (c) 2022 Shuhei Nitta. All rights reserved.
import re
import time
import dataclasses
import typing as t

from selenium.webdriver.common import by
import requests
import bs4

from yahoo_auction_auto import urls, info, webdriver, cookie


@dataclasses.dataclass()
class YahooAuction:
    """API for Yahoo!Auction."""
    cookies: list[cookie.Cookie] = dataclasses.field(default_factory=list)
    """Cookies to get a session."""
    timeout: int = 60
    """Time to wait for a response in second."""
    chrome_args: t.Iterable[str] = dataclasses.field(default_factory=list)
    """Arguments for Chrome."""

    @property
    def cookies_for_requests(self) -> dict[str, str]:
        """Cookies for `requests` module."""
        return {cookie["name"]: cookie["value"] for cookie in self.cookies}

    @property
    def chrome_options(self) -> webdriver.ChromeOptions:
        options = webdriver.ChromeOptions()
        for arg in self.chrome_args:
            options.add_argument(arg)
        return options

    @property
    def is_login(self) -> bool:
        """Whether its cookies is valid to log in."""
        url = urls.MYPAGE
        try:
            response = requests.get(
                url,
                cookies=self.cookies_for_requests,
                timeout=self.timeout
            )
            response.raise_for_status()
        except Exception:
            return False
        return bool(response.url == url)

    @property
    def urls_selling(self) -> list[str]:
        """URLs of items currently selling on Yahoo!Auction."""
        pattern = r"^rsec:itm;slk:tc;"
        return _get_urls(self.cookies_for_requests, urls.SELLING, pattern)

    @property
    def aIDs_selling(self) -> list[str]:
        """Auction IDs of items currently selling on Yahoo!Auction."""
        pattern = re.compile(r'(?<=/)\w+$')
        return [match[0] for match in map(pattern.search, self.urls_selling) if match]

    @property
    def urls_closed_with_winner(self) -> list[str]:
        """URLs of items closed with winner on Yahoo!Auction."""
        pattern = r"^rsec:itm;slk:ttlc;"
        return _get_urls(self.cookies_for_requests, urls.CLOSED_WITH_WINNER, pattern)

    @property
    def aIDs_closed_with_winner(self) -> list[str]:
        """Auction IDs of items closed with winner on Yahoo!Auction."""
        pattern = re.compile(r'(?<=/)\w+$')
        return [match[0] for match in map(pattern.search, self.urls_closed_with_winner) if match]

    @property
    def urls_closed_without_winner(self) -> list[str]:
        """URLs of items closed with no winner on Yahoo!Auction."""
        pattern = r'^rsec:itm;slk:ttlc;'
        return _get_urls(self.cookies_for_requests, urls.CLOSED_WITHOUT_WINNER, pattern)

    @property
    def aIDs_closed_without_winner(self) -> list[str]:
        """Auction IDs of items closed with no winner on Yahoo!Auction."""
        pattern = re.compile(r'(?<=/)\w+$')
        return [match[0] for match in map(pattern.search, self.urls_closed_without_winner) if match]

    def submit(self) -> None:
        """Submit an item on Yahoo!Auction.

        Not Impremented yet.
        """
        raise NotImplementedError()

    def cancel(self, aID: str) -> None:
        """Cancel a sale of an item.

        Parameters
        ----------
        aID : str
            The auction ID of the item to cancel.
        """
        with webdriver.chrome(self.chrome_options) as driver:
            driver.get(urls.HOME)
            url = driver.current_url
            for _cookie in self.cookies:
                driver.add_cookie(_cookie)
            driver.get(urls.get_cancel_url(aID))
            cancel_element = driver.find_element(by.By.NAME, "confirm")
            cancel_element.click()
            while url == driver.current_url:
                time.sleep(0.5)

    def resubmit(self, aID: str) -> None:
        """Resubmit an item.

        Parameters
        ----------
        aID : str
            The auction ID of the item to resubmit.

        Not Inpremented yet.
        """
        raise NotImplementedError()

    def get_info_selling(self, aID: str) -> info.InfoSelling:
        """Get information of an item currently selling.

        Parameters
        ----------
        aID : str
            The auction ID of an item.

        Returns
        -------
        yahoo_auction_aucto.info.InfoSelling
            The information of the product.
        """
        url = urls.get_auction_url(aID)
        response = requests.get(
            url,
            cookies=self.cookies_for_requests,
            timeout=self.timeout
        )
        soup = bs4.BeautifulSoup(response.content, "lxml")
        return info.InfoSelling.fromsoup(soup)

    def get_info_closed_with_winner(self) -> info.InfoClosedWithWinner:
        """Get information of an item closed with a winner.

        Parameters
        ----------
        aID : str
            The auction ID of an item.

        Returns
        -------
        yahoo_auction_aucto.info.InfoClosedWithWinner
            The information of the product.

        Not Impremented yet.
        """
        raise NotImplementedError()

    def get_info_closed_without_winner(self) -> info.InfoClosedWithoutWinner:
        """Get information of an item closed without a winner.

        Parameters
        ----------
        aID : str
            The auction ID of an item.

        Returns
        -------
        yahoo_auction_aucto.info.InfoClosedWithoutWinner
            The information of the product.

        Not Impremented yet.
        """
        raise NotImplementedError()


def _get_urls(cookies: dict[str, str], src_url: str, pattern: str | t.Pattern[str]) -> list[str]:
    """Get product urls from `src_url`.

    Recursive.
    """
    response = requests.get(src_url, cookies=cookies)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.content, "lxml")
    urls: list[str] = []
    for tag in soup.find_all("a", attrs={"data-ylk": pattern}):
        if isinstance(tag, bs4.Tag):
            if url := tag.get("href", None):
                if isinstance(url, str):
                    urls.append(url)
                elif isinstance(url, list):
                    urls.extend(url)
    if next_page := _get_next_page(soup):
        urls.extend(_get_urls(cookies, next_page, pattern))
    return urls


def _get_next_page(soup: bs4.BeautifulSoup) -> t.Optional[str]:
    """Get the next page url from `soup`.

    Parameters
    ----------
    soup : bs4.BeautifulSoup
        The soup of a Yahoo!Auction page.

    Returns
    -------
    str | None
        URL of next page if exists, else None.
    """
    pattern = r'^rsec:pagination;slk:next;'
    if next_page_tag := soup.find("a", attrs={"data-ylk": pattern}):
        if isinstance(next_page_tag, bs4.Tag):
            href = next_page_tag.get("href", None)
            if isinstance(href, list):
                return href.pop()
            else:
                return href
    return None
