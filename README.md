# ヤフオク！のタスクを自動化

## 必要要件

- Python3.10 以上
- Google Chrome / Chromium

## インストール

```sh
$ pip install yahoo-auction-auto
# または
$ pip install git+https://github.com/huisint/yahoo-auction-auto
```

## 使用方法

このパッケージでは廃止された公式 API の代わりに cookie を使ってセッションを取得する。
取得したcookieを使用して、出品情報を取得する。

```python
>>> import yahoo_auction_auto as yaa
>>> cookies = yaa.get_cookies()
>>> yah = yaa.YahooAuction(cookies)
>>> aIDs = yah.aIDs_selling           # 出品中のaIDを全て取得する
>>> for aID in aIDs[:3]:
...     info = ya.get_info_selling(aID)  # 出品中の情報を取得する。
...     print(info.__dict__)
```

## License
MIT License
