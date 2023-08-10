from http import HTTPStatus
import string
import os
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
    ''' Error that will be raised if converting a ticker is not succesfull'''
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return f"[{self.response}] - Failed to fetch ticker symbol"


class YahooRequests:
    ''' The class for YahooRequests, having different features for stock extracting'''
    
    @staticmethod
    def remove_suffix(name):
        suffixes = [
                    "corp.", ",", "co.",
                    "ltd.", "plc", "sa", "ag",
                    " &", "inc.", "(the)", "ord", "sh",
                    "inc"
                    ]
        for suffix in suffixes:
            name = name.lower().replace(suffix, "")
        return string.capwords(name, sep=None)
    
    @staticmethod
    def converted_currency(price: int, currency: str) -> int:
        ''' Convert the price to a different currency using OER'''
        # Acces the workflow defined OER Key using os
        api_key = os.environ["OER"]
        # Use the OpenExhangeRates api to get current currency rates
        url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
        # Use requests to define as variable
        response = requests.get(url, timeout=10)
        # Convert to json format so it is indexable
        data = response.json()
        # Unpack currency
        if isinstance(currency, list):
            unpacked_currency = currency[0]    
        else:
            unpacked_currency = currency
        # Index to the location of the uppercase version of the chosen curreny
        converted_price = data["rates"][unpacked_currency.upper()] * price
        return round(converted_price, 2)

    @staticmethod
    def request_ticker_info(ticker: str) -> dict:
        """
        Fetches the data for the desired ticker symbol

        Raises ConversionError if the request wasn't successful.
        """

        response = requests.get(API_URL_TEMPLATE.format(ticker=ticker), headers=HEADERS, timeout=10)

        if response.status_code != HTTPStatus.OK:
            raise ConversionError(f"[{response.status_code}] - Failed to fetch ticker symbol")

        try:
            # Convert to Json format and find price
            data = response.json()['optionChain']['result'][0]['quote']
        except IndexError as exc:
            # If price could not be found raise conversionerror
            # This may occur because the ticker is incorrect or non-existand
            raise ConversionError(response.status_code) from exc
        return data

    @classmethod
    def price(cls, ticker: str, *convert_currency) -> int:
        '''
        Gets the current price of the stock with the given ticker symbol.

        Raises ConversionError if the ticker symbol is invalid.
        '''
        try:
            price_usd = cls.request_ticker_info(ticker)['regularMarketPrice']
        except LookupError:
            raise ConversionError(ticker)
        if convert_currency:
            return cls.converted_currency(price_usd, convert_currency)
        else:
            return price_usd

    @classmethod
    def name(cls, ticker: str, remove_suffix=False) -> str:
        """
        Gets the company name of the stock with the given ticker symbol.

        Raises ConversionError if the ticker symbol is invalid.
        """
        try:
            name = cls.request_ticker_info(ticker)['shortName']
        except LookupError:
            raise ConversionError(ticker)
        # Check if the name only consist of numbers, and therefore is not what the user is looking for
        if name.isnumeric():
            raise ConversionError(f"{ticker} fetches number instead of str")
        else:
            if remove_suffix is not False:
                return cls.remove_suffix(name)
            else:
                return name
