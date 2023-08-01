from http import HTTPStatus
import requests

API_URL_TEMPLATE = 'https://query1.finance.yahoo.com/v7/finance/options/{ticker}'

# Yahoo's api was shut down in 2017 so making a header is required to look like a browser
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (X11; Linux x86_64)'
        ' AppleWebKit/537.36 (KHTML, like Gecko)'
        ' Chrome/108.0.0.0 Safari/537.36'
    )
}


class ConversionError(Exception):
    """Ticker could not be converted to company name, please contact the creator"""


class YahooRequests:

    @staticmethod
    def request_ticker_info(ticker: str) -> dict:
        """
        Fetches the data for the desired ticker symbol

        Raises ConversionError if the request wasn't successful.
        """

        response = requests.get(API_URL_TEMPLATE.format(ticker=ticker), headers=HEADERS)

        if response.status_code != HTTPStatus.OK:
            raise ConversionError(f"[{response.status_code}] - Failed to fetch ticker symbol")

        data = response.json()
        return data['optionChain']['result'][0]['quote']

    @classmethod
    def price(cls, ticker: str) -> int:
        '''
        Gets the current price of the stock with the given ticker symbol.

        Raises ConversionError if the ticker symbol is invalid.
        '''
        return cls.request_ticker_info(ticker)['regularMarketPrice']

    @classmethod
    def name(cls, ticker: str) -> str:
        """
        Gets the company name of the stock with the given ticker symbol.

        Raises ConversionError if the ticker symbol is invalid.
        """
        return cls.request_ticker_info(ticker)['shortName']
