import threading
import requests
from lxml import html


class Stock(threading.Thread):
    def __init__(self, symbol: str) -> None:
        super().__init__()

        self.symbol = symbol
        self.url = f'https://finance.yahoo.com/quote/{symbol}'
        self.price = None

    def run(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        response = requests.get(self.url, headers=headers)
        if response.status_code == 200:
            # parse the HTML
            tree = html.fromstring(response.text)
            # get the price in text
            price_text = tree.xpath(
                '//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[1]/text()')
            if price_text:
                try:
                    self.price = float(price_text[0].replace(',', ''))
                except ValueError:
                    self.price = None

    def __str__(self):
        return f'{self.symbol}\t{self.price}'


symbols = ['MSFT', 'GOOGL', 'AAPL', 'META']
threads = []

for symbol in symbols:
    t = Stock(symbol)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
    print(t)

"""
Sometimes, you may want to execute a task in the background. To do that you use a special kind of thread called a daemon thread.

By definition, daemon threads are background threads. In other words, daemon threads execute tasks in the background.
Daemon threads are helpful for executing tasks that support non-daemon threads in the program. For example:

Log information to a file in the background.
Scrap contents from a website in the background.
Auto-save the data into a database in the backgro

"""