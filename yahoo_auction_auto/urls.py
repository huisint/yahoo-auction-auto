# Copyright (c) 2022 Shuhei Nitta. All rights reserved.

HOME = "https://yahoo.co.jp"
MYPAGE = "https://auctions.yahoo.co.jp/user/jp/show/mystatus"
SELLING = "https://auctions.yahoo.co.jp/openuser/jp/show/mystatus?select=selling"
CLOSED_WITH_WINNER = "https://auctions.yahoo.co.jp/closeduser/jp/show/mystatus?select=closed&hasWinner=1"
CLOSED_WITHOUT_WINNER = "https://auctions.yahoo.co.jp/closeduser/jp/show/mystatus?select=closed&hasWinner=0"


def get_auction_url(aID: str) -> str:
    return f"https://page.auctions.yahoo.co.jp/jp/auction/{aID}"


def get_cancel_url(aID: str) -> str:
    return f"https://page.auctions.yahoo.co.jp/jp/show/cancelauction?aID={aID}"
