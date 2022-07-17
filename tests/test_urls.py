# Copyright (c) 2022 Shuhei Nitta. All rights reserved.
from unittest import TestCase

from yahoo_auction_auto import urls


class Test_get_auction_url(TestCase):

    def setUp(self) -> None:
        self.urlbase = "https://page.auctions.yahoo.co.jp/jp/auction/{aID}"

    def test_aID(self) -> None:
        aIDs = ["1000000000", "cndskxhflso", "h2l9494f14"]
        for aID in aIDs:
            with self.subTest(aID=aID):
                self.assertEqual(
                    urls.get_auction_url(aID),
                    self.urlbase.format(aID=aID)
                )


class Test_get_cancel_url(TestCase):

    def setUp(self) -> None:
        self.urlbase = "https://page.auctions.yahoo.co.jp/jp/show/cancelauction?aID={aID}"

    def test_aID(self) -> None:
        aIDs = ["1000000000", "cndskxhflso", "h2l9494f14"]
        for aID in aIDs:
            with self.subTest(aID=aID):
                self.assertEqual(
                    urls.get_cancel_url(aID),
                    self.urlbase.format(aID=aID)
                )
