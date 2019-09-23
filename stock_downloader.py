"""
stock_downloader.py
~~~~~~~~~~~~~~~~~~~~
A stock price downloader.
"""
import io
import re
import socket
import requests
from typing import List, Optional, Mapping, Dict, NoReturn, NewType, Type, TypeVar, Tuple


class StockDownloader(object):
    """Downloads the stock prices from a given url."""

    def __init__(self) -> NoReturn:
        self.urls: Dict[str, str] = {}
        self.stocks: Dict[str, str]  = {}
        self.periods: List[Tuple[str, str]] = []
        self.intervals: List[str] = []


    def set_stocks(self, **kwargs) -> NoReturn:
        """Set the stocks that will be searched."""
        try:
            for k in kwargs:
                self.stocks[k] = kwargs[k]
        except Exception as e:
            print(e)

    def set_urls(self, **kwargs) -> NoReturn:
        """Set the urls that will be searched."""
        try:
            for k in kwargs:
                self.urls[k] = kwargs[k]
        except Exception as e:
            print(e)

    def set_periods(self, *args, **kwargs) -> NoReturn:
        """Set the time period ranges that will be used."""
        try:
            pass
        except Exception as e:
            print(e)

    def set_interval(self, *args, **kwargs) -> NoReturn:
        """Set the time interval, ie. 1d, 1wk, 1mo"""
        try:
            pass
        except Exception as e:
            print(e)


sd = StockDownloader()
sd.set_urls(yahoo='finance.yahoo.com/quote', google='google.com')
sd.set_stocks(apple='AAPL', microsoft='MSFT', phressia='PHR', intel='INTC')
print(sd.urls)
