# Copyright (c) 2022 Shuhei Nitta. All rights reserved.
import re
import datetime
import dataclasses

import bs4


@dataclasses.dataclass(frozen=True)
class InfoSelling:
    aID: str
    """The auction ID."""
    title: str
    """The title of an auction."""
    seller_name: str
    """The seller name of an auction."""
    stock: int
    """The number of stocks of an auction."""
    start_datetime: datetime.datetime
    """When an auction starts."""
    end_datetime: datetime.datetime
    """When an auction ends."""
    refundable: bool
    """Whether an auction is refundable."""
    startprice: str
    """The start price of an auction."""
    timeleft: str
    """The timeleft of an auction."""
    count_bid: int
    """The number of bids."""
    count_access: int
    """The number of accesses."""
    count_watch: int
    """The number of watches"""

    @classmethod
    def fromsoup(cls, soup: bs4.BeautifulSoup) -> "InfoSelling":
        return cls(
            _get_aID(soup),
            _get_title(soup),
            _get_seller_name(soup),
            _get_stock(soup),
            _get_start_datetime(soup),
            _get_end_datetime(soup),
            _get_refundable(soup),
            _get_startprice(soup),
            _get_timeleft(soup),
            _get_count_bid(soup),
            _get_count_access(soup),
            _get_count_watch(soup),
        )


# Scraping functions
# The soup is from YahooAuctionURL.AUCTION()
def _get_aID(soup: bs4.BeautifulSoup) -> str:
    """Get the auction ID of an auction from `soup`.

    Parameters
    ----------
    soup : bs4.BeautifulSoup
        A soup of a Yahoo!Auction page.

    Returns
    -------
    str
        The auction ID of the auction.
    """
    if tag := soup.find("dt", string="オークションID"):
        if isinstance(tag, bs4.Tag):
            tag = tag.find_next_sibling("dd", {"class": "ProductDetail__description"})
            if isinstance(tag, bs4.Tag):
                return str(tag.text.strip("："))
    return ""


def _get_title(soup: bs4.BeautifulSoup) -> str:
    """Get the title of an auction from `soup`.

    Parameters
    ----------
    soup : bs4.BeautifulSoup
        A soup of a Yahoo!Auction page.

    Returns
    -------
    str
        The title of the auction.
    """
    if title := soup.find("h1", {"class": "ProductTitle__text"}):
        if isinstance(title, bs4.Tag):
            return str(title.text)
    return ""


def _get_seller_name(soup: bs4.BeautifulSoup) -> str:
    """Get the seller name of an auction from `soup`.

    Parameters
    ----------
    soup : bs4.BeautifulSoup
        A soup of a Yahoo!Auction page.

    Returns
    -------
    str
        The seller name of the auction.
    """
    pattern = re.compile(r'^rsec:seller;slk:slfinfo;')
    if seller_name := soup.find("a", {"data-ylk": pattern}):
        if isinstance(seller_name, bs4.Tag):
            return str(seller_name.text)
    return ""


def _get_stock(soup: bs4.BeautifulSoup) -> int:
    """Get the stock count of an auction from `soup`.

    Parameters
    ----------
    soup : bs4.BeautifulSoup
        A soup of a Yahoo!Auction page.

    Returns
    -------
    int
        The stock count of the auction.
    """
    if tag := soup.find("dt", string="個数"):
        if isinstance(tag, bs4.Tag):
            tag = tag.find_next_sibling("dd", {"class": "ProductDetail__description"})
            if isinstance(tag, bs4.Tag):
                return int(tag.text.strip("："))
    return 0


def _from_yahoo_datetime(datetimestr: str) -> datetime.datetime:
    """Get datetime.datetime instance from format `YYYY.MM.DD（d）HH:MM`

    Parameters
    ----------
    datetimestr : str
        A string of datetime on a Yahoo!Auction page.

    Returns
    -------
    datetime.datetime
    """
    year: int = int(datetimestr[:4])
    month: int = int(datetimestr[5:7])
    day: int = int(datetimestr[8:10])
    hour: int = int(datetimestr[13:15])
    min: int = int(datetimestr[16:18])
    return datetime.datetime(year, month, day, hour, min)


def _get_start_datetime(soup: bs4.BeautifulSoup) -> datetime.datetime:
    """Get start datetime of an auction from `soup`.

    Parameters
    ----------
    soup : bs4.BeautifulSoup
        A soup of a Yahoo!Auction page.

    Returns
    -------
    datetime.datetime
        The start datetime of the auction.
    """
    if tag := soup.find("dt", string="開始日時"):
        if isinstance(tag, bs4.Tag):
            tag = tag.find_next_sibling("dd", {"class": "ProductDetail__description"})
            if isinstance(tag, bs4.Tag):
                return _from_yahoo_datetime(tag.text.strip("："))
    return datetime.datetime(1970, 1, 1)


def _get_end_datetime(soup: bs4.BeautifulSoup) -> datetime.datetime:
    """Get start datetime of an auction from `soup`.

    Parameters
    ----------
    soup : bs4.BeautifulSoup
        A soup of a Yahoo!Auction page.

    Returns
    -------
    datetime.datetime
        The end datetime of the auction.
    """
    if tag := soup.find("dt", string="終了日時"):
        if isinstance(tag, bs4.Tag):
            tag = tag.find_next_sibling("dd", {"class": "ProductDetail__description"})
            if isinstance(tag, bs4.Tag):
                return _from_yahoo_datetime(tag.text.strip("："))
    return datetime.datetime(1970, 1, 1)


def _get_refundable(soup: bs4.BeautifulSoup) -> bool:
    """Return true if an auction from `soup` is refundable.

    Parameters
    ----------
    soup : bs4.BeautifulSoup
        A soup of a Yahoo!Auction page.

    Returns
    -------
    bool
        Return true if the auction is refundable.
    """
    if tag := soup.find("dt", string="返品"):
        if isinstance(tag, bs4.Tag):
            tag = tag.find_next_sibling("dd", {"class": "ProductDetail__description"})
            if isinstance(tag, bs4.Tag):
                return bool(tag.text.strip("：") != "返品不可")
    return False


def _get_startprice(soup: bs4.BeautifulSoup) -> str:
    """Get the start price of an auction from `soup`.

    Parameters
    ----------
    soup : bs4.BeautifulSoup
        A soup of a Yahoo!Auction page.

    Returns
    -------
    str
        The start price of the auction. e.g. 10,000 円（税 0 円）
    """
    if tag := soup.find("dt", string="開始価格"):
        if isinstance(tag, bs4.element.Tag):
            tag = tag.find_next_sibling("dd", {"class": "ProductDetail__description"})
            if isinstance(tag, bs4.Tag):
                return str(tag.text.strip("："))
    return ""


def _get_timeleft(soup: bs4.BeautifulSoup) -> str:
    """Get the timeleft of an auction from `soup`.

    Parameters
    ----------
    soup : bs4.BeautifulSoup
        A soup of a Yahoo!Auction page.

    Returns
    -------
    str
        A string of timeleft of the auction.
    """
    if tag := soup.find("dt", string="残り時間"):
        if isinstance(tag, bs4.element.Tag):
            tag = tag.find_next_sibling("dd", {"class": "Count__number"})
            if isinstance(tag, bs4.Tag):
                return str(tag.text.splitlines()[0])
    return ""


def _get_count_bid(soup: bs4.BeautifulSoup) -> int:
    """Get the bidding count of an auction from `soup`.

    Parameters
    ----------
    soup : bs4.BeautifulSoup
        A soup of a Yahoo!Auction page.

    Returns
    -------
    int
        The total count of bidding for the auction.
    """
    if tag := soup.find("dt", string="入札件数"):
        if isinstance(tag, bs4.element.Tag):
            tag = tag.find_next_sibling("dd", {"class": "Count__number"})
            if isinstance(tag, bs4.Tag):
                return int(tag.text[:-4])
    return 0


def _get_count_access(soup: bs4.BeautifulSoup) -> int:
    """Get the access count of an auction from `soup`.

    Parameters
    ----------
    soup : bs4.BeautifulSoup
        A soup of a Yahoo!Auction page.

    Returns
    -------
    int
        The total count of access of the auction.
    """
    if tag := soup.find("span", {"class": "StatisticsInfo__term--access"}):
        if isinstance(tag, bs4.element.Tag):
            tag = tag.find_next_sibling("span", {"class": "StatisticsInfo__data"})
            if isinstance(tag, bs4.Tag):
                return int(tag.text)
    return 0


def _get_count_watch(soup: bs4.BeautifulSoup) -> int:
    """Get the watch count of an auction from `soup`.

    Parameters
    ----------
    soup : bs4.BeautifulSoup
        A soup of a Yahoo!Auction page.

    Returns
    -------
    int
        The total count of watch for the auction.
    """
    if tag := soup.find("span", {"class": "StatisticsInfo__term--watch"}):
        if isinstance(tag, bs4.element.Tag):
            tag = tag.find_next_sibling("span", {"class": "StatisticsInfo__data"})
            if isinstance(tag, bs4.Tag):
                return int(tag.text)
    return 0
