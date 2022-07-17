# Copyright (c) 2022 Shuhei Nitta. All rights reserved.
from unittest import TestCase
import datetime
import functools

import bs4

from yahoo_auction_auto.info import selling


@functools.lru_cache(maxsize=32)
def load_file(filename: str) -> str:
    with open(filename, encoding="utf-8") as f:
        return f.read()


class TestInfoSelling_fromsoup(TestCase):

    def setUp(self) -> None:
        self.test_filename = "tests/info/test_selling.html"
        self.soup = bs4.BeautifulSoup(load_file(self.test_filename), "lxml")
        self.soup_empty = bs4.BeautifulSoup("", "lxml")

    def test_aID(self) -> None:
        with self.subTest(self.test_filename):
            info = selling.InfoSelling.fromsoup(self.soup)
            self.assertEqual(info.aID, "10000000000")
        with self.subTest("empty"):
            info = selling.InfoSelling.fromsoup(self.soup_empty)
            self.assertEqual(info.aID, "")

    def test_title(self) -> None:
        with self.subTest(self.test_filename):
            info = selling.InfoSelling.fromsoup(self.soup)
            self.assertEqual(info.title, "title")
        with self.subTest("empty"):
            info = selling.InfoSelling.fromsoup(self.soup_empty)
            self.assertEqual(info.title, "")

    def test_seller_name(self) -> None:
        with self.subTest(self.test_filename):
            info = selling.InfoSelling.fromsoup(self.soup)
            self.assertEqual(info.seller_name, "seller_name")
        with self.subTest("empty"):
            info = selling.InfoSelling.fromsoup(self.soup_empty)
            self.assertEqual(info.seller_name, "")

    def test_stock(self) -> None:
        with self.subTest(self.test_filename):
            info = selling.InfoSelling.fromsoup(self.soup)
            self.assertEqual(info.stock, 1)
        with self.subTest("empty"):
            info = selling.InfoSelling.fromsoup(self.soup_empty)
            self.assertEqual(info.stock, 0)

    def test_start_datetime(self) -> None:
        with self.subTest(self.test_filename):
            info = selling.InfoSelling.fromsoup(self.soup)
            self.assertEqual(
                info.start_datetime,
                datetime.datetime(2021, 10, 12, 19, 54)
            )
        with self.subTest("empty"):
            info = selling.InfoSelling.fromsoup(self.soup_empty)
            self.assertEqual(
                info.start_datetime,
                datetime.datetime(1970, 1, 1, 0, 0)
            )

    def test_end_datetime(self) -> None:
        with self.subTest(self.test_filename):
            info = selling.InfoSelling.fromsoup(self.soup)
            self.assertEqual(
                info.end_datetime,
                datetime.datetime(2021, 10, 15, 19, 54)
            )
        with self.subTest("empty"):
            info = selling.InfoSelling.fromsoup(self.soup_empty)
            self.assertEqual(
                info.end_datetime,
                datetime.datetime(1970, 1, 1, 0, 0)
            )

    def test_refundable(self) -> None:
        with self.subTest(self.test_filename):
            info = selling.InfoSelling.fromsoup(self.soup)
            self.assertTrue(info.refundable)
        with self.subTest("empty"):
            info = selling.InfoSelling.fromsoup(self.soup_empty)
            self.assertFalse(info.refundable)

    def test_get_detail_startprice(self) -> None:
        with self.subTest(self.test_filename):
            info = selling.InfoSelling.fromsoup(self.soup)
            self.assertEqual(info.startprice, "10,000 円（税 0 円）")
        with self.subTest("empty"):
            info = selling.InfoSelling.fromsoup(self.soup_empty)
            self.assertEqual(info.startprice, "")

    def test_timeleft(self) -> None:
        with self.subTest(self.test_filename):
            timeleft: str = selling._get_timeleft(self.soup)
            self.assertEqual(timeleft, "19時間")
        with self.subTest("empty"):
            info = selling.InfoSelling.fromsoup(self.soup_empty)
            self.assertEqual(info.timeleft, "")

    def test_count_bid(self) -> None:
        with self.subTest(self.test_filename):
            info = selling.InfoSelling.fromsoup(self.soup)
            self.assertEqual(info.count_bid, 1)
        with self.subTest("empty"):
            info = selling.InfoSelling.fromsoup(self.soup_empty)
            self.assertEqual(info.count_bid, 0)

    def test_count_access(self) -> None:
        with self.subTest(self.test_filename):
            info = selling.InfoSelling.fromsoup(self.soup)
            self.assertEqual(info.count_access, 2)
        with self.subTest("empty"):
            info = selling.InfoSelling.fromsoup(self.soup_empty)
            self.assertEqual(info.count_access, 0)

    def test_count_watch(self) -> None:
        with self.subTest(self.test_filename):
            info = selling.InfoSelling.fromsoup(self.soup)
            self.assertEqual(info.count_watch, 3)
        with self.subTest("empty"):
            info = selling.InfoSelling.fromsoup(self.soup_empty)
            self.assertEqual(info.count_watch, 0)
