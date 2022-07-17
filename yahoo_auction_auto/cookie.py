# Copyright (c) 2022 Shuhei Nitta. All rights reserved.
import time
import typing as t

from selenium.webdriver.common import by

from yahoo_auction_auto import urls, webdriver


Cookie = dict[str, t.Any]


def get_cookies(chrome_args: t.Iterable[str] | None = None) -> list[Cookie]:
    """Get cookies of Yahoo!Auction.

    Parameters
    ----------
    chrome_args : Iterable[str] | None
        Arguments of Chrome.

    Returns
    -------
    list[yahoo_auction_auto.cookie.Cookie]
    """
    _, cookies = get_username_and_cookies(chrome_args)
    return cookies


def get_username_and_cookies(chrome_args: t.Iterable[str] | None = None) -> tuple[str, list[Cookie]]:
    """Get username and cookies of Yahoo!Auction.

    Parameters
    ----------
    chrome_args : Iterable[str] | None
        Arguments of Chrome.

    Returns
    -------
    username : str
        The username
    cookies : list[yahoo_auction_auto.cookie.Cookie]
        The cookies
    """
    chrome_options = webdriver.ChromeOptions()
    for arg in chrome_args or []:
        chrome_options.add_argument(arg)
    with webdriver.chrome(chrome_options) as driver:
        driver.get(urls.MYPAGE)
        while driver.current_url != urls.MYPAGE:
            time.sleep(1)
        username = driver \
            .find_element(by.By.CLASS_NAME, "yjmthloginarea") \
            .find_element(by.By.TAG_NAME, "strong") \
            .text
        cookies = driver.get_cookies()  # type: ignore
    return str(username), list(cookies)
