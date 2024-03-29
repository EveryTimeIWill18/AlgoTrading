"""
stock_downloader.py
~~~~~~~~~~~~~~~~~~~~
A stock price downloader.
"""
import io
import re
import ssl
import socket
import requests
from pprint import pprint
from itertools import chain
from bs4 import BeautifulSoup
from typing import List, Optional, Mapping, Dict, NoReturn, NewType, Type, TypeVar, Tuple, Text, ByteString, AnyStr, Any

Integer = NewType('Integer', int)


class HttpRequest(object):
    """Creates an http request using ssl and sockets"""

    def __init__(self):
        self._url: str = None
        self._host: str = None
        self._port: int = None
        self.raw_data: bytes = b""

    @property
    def url(self) -> ByteString:
        return self._url

    @url.setter
    def url(self, url) -> NoReturn:
        self._url = url

    @property
    def host(self) -> AnyStr:
        return self._host

    @host.setter
    def host(self, host):
        self._host = host

    @property
    def port(self) -> Integer:
        return self._port

    @port.setter
    def port(self, port) -> NoReturn:
        self._port = port


    def make_http_request(self, chunk_size: int,  timeout=5):
        """Create the http request."""
        try:
            socket.setdefaulttimeout(timeout)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))

            s = ssl.wrap_socket(s, keyfile=None, server_side=False, cert_reqs=ssl.CERT_NONE,
                                ssl_version=ssl.PROTOCOL_SSLv23)

            http_str = f"GET {self.url} HTTP/1.1\r\nHost: {self.host}\r\n\r\n"
            s.sendall(http_str.encode())

            while True:
                chunk = s.recv(chunk_size)
                if not chunk:
                    break
                self.raw_data += chunk

            self.raw_data = self.raw_data.decode(encoding='utf-8', errors='ignore')
        except Exception as e:
            print(e)




class StockDownloader(object):
    """Downloads the stock prices from a given url."""

    def __init__(self) -> NoReturn:
        self.stocks: Dict[str, str]  = {}
        self.periods: List[Tuple[str, str]] = []
        self.intervals: List[str] = ['1d', '1wk', '1mo']
        self.filters: List[str] = ['history', 'div', 'split']
        self.urls: List[str] = []
        self.data_set: Dict[str, Dict[str, Any]] = {}


    def set_stocks(self, **kwargs) -> NoReturn:
        """Set the stocks that will be searched."""
        try:
            for k in kwargs:
                self.stocks[k] = kwargs[k]
        except Exception as e:
            print(e)


    def set_time_periods(self, *args) -> NoReturn:
        """Set the time period ranges that will be used."""
        try:
            t = tuple()
            for a in args:
                if len(t) < 2:
                    t = t + (a,)
                if len(t) == 2:
                    self.periods.append(t)
                    del t
                    t = tuple()
        except Exception as e:
            print(e)

    def create_payload_string(self) -> Text:
        """Create's the payload string that is sent out during the request"""
        payload = f"""https://finance.yahoo.com/quote/{self.stocks['apple']}/history?period1={self.periods[0][0]}&period2={self.periods[0][1]}&interval={self.intervals[0]}&filter={self.filters[0]}&frequency={self.intervals[0]}"""
        return payload


    def download_stock_data(self) -> Mapping[str, List[str]]:
        """Download the stock data information"""

        r = requests.get(self.create_payload_string())
        if r.status_code == 200:
            print(r.url)
            content = r.content.__str__()
            soup = BeautifulSoup(content, 'html.parser')
            # print(soup.prettify())

            # extract the dates, values[Open, High, Low, Close*, Adj Close**, Volume]
            date_re = re.compile(r'<span\sdata-reactid="\d{1,3}">([A-S]\w{1,4}\s\d{2},\s\d{4})')
            values_re = re.compile(r'<span\sdata-reactid="\d{1,3}">(\d{1,7}\.\d{0,10})')
            volume_re = re.compile(r'<span\sdata-reactid="\d{1,3}">(\d{1,3}?,\d{1,3}?,\d{1,3})')

            # load in the data
            dates = date_re.findall(content)
            values = values_re.findall(content)
            volumes = volume_re.findall(content)

            extracted_data = {'Dates': dates, 'Values': values, 'Volumes': volumes}
            return extracted_data

    def reformat_stock_data(self):
        """Reformat the extracted stock data into a usable form"""
        stocks = self.download_stock_data()
        self.data_set = {stocks['Dates'][i]: {'Open': [], 'High': [], 'Low': [], 'Close': [], 'Adj Close': [],
                             'Volume': int(stocks['Volumes'][i].replace(',' ,''))}
                        for i, _ in enumerate(stocks['Dates'])}
        value_counter = 0
        for k in list(self.data_set.keys()):
            current_date = self.data_set[k]
            counter = 0
            while counter < 5:
                if counter == 0:
                    current_date["Open"] = float(stocks["Values"][value_counter])
                if counter == 1:
                    current_date["High"] = float(stocks["Values"][value_counter])
                if counter == 2:
                    current_date["Low"] = float(stocks["Values"][value_counter])
                if counter == 3:
                    current_date["Close"] = float(stocks["Values"][value_counter])
                if counter == 4:
                    current_date["Adj Close"] = float(stocks["Values"][value_counter])
                value_counter += 1
                counter += 1

















sd = StockDownloader()
sd.set_stocks(apple='AAPL', microsoft='MSFT', phressia='PHR', intel='INTC')
sd.set_time_periods(1568865600, 1569902400, 1000000, 2000000)
payload = sd.create_payload_string()
stocks = sd.download_stock_data()
for k in stocks.keys():
    print(k, len(stocks[k]))
sd.reformat_stock_data()
pprint(sd.data_set)
#pprint(sd.data_set)
#pprint(list(sd.data_set['Sep 20, 2019'].keys()))



# http_socket = HttpRequest()
# http_socket.url = "https://finance.yahoo.com/quote/AAPL/history?period1=1553400000&period2=1569297600&interval=1d&filter=history&frequency=1d"
# http_socket.host = "www.finance.yahoo.com"
# http_socket.port = 443
# http_socket.make_http_request(chunk_size=2048, timeout=10)