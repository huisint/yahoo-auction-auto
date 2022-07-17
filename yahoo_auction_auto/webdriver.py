# Copyright (c) 2022 Shuhei Nitta. All rights reserved.
import contextlib
import typing as t

from selenium import webdriver
import chromedriver_binary  # noqa


ChromeOptions = webdriver.ChromeOptions


@contextlib.contextmanager
def chrome(options: webdriver.ChromeOptions) -> t.Iterator[webdriver.Chrome]:
    options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    try:
        yield driver
    finally:
        driver.quit()
