
'''This is a module for extracitng stock data from Yahoo Finance

    An more in-depth guide is in the README file
'''

from http import HTTPStatus
import string
import os
import datetime
import requests
from tabulate import tabulate


API_URL_TEMPLATE = "https://query1.finance.yahoo.com/v7/finance/options/{ticker}"

# Yahoo's api was shut down in 2017 so making a header is required to look like a browser
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64)"
        " AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/108.0.0.0 Safari/537.36"
    )
}


class ConversionError(Exception):
    """Error that will be raised if converting a ticker is not succesfull."""

    def __init__(self, response):
        """Response is set."""
        self.response = response

    def __str__(self):
        """Define the standart response."""
        return f"[{self.response}] - Failed to fetch ticker symbol"


class YahooRequests:
    """The class YahooRequests, having different features for stock extracting."""

    index = -1

    @classmethod
    def basic_info(cls, ticker: str, dictionary=False) -> str | dict:
        """Give table with the values of the compnay and other information."""
        response = cls.request_ticker_info(ticker)
        if not dictionary:
            table = [
                ["Name: ", cls.name(ticker)],
                ["Current price: ", f"${cls.price(ticker, convert_currency='usd')}"],
                ["Region: ", response["region"]],
                ["Language: ", response["language"]],
                ["Exchange: ", response["fullExchangeName"]],
                ["Average analyst rating: ", response["averageAnalystRating"]],
                ["Fifty day average price: ", response["fiftyDayAverage"]],
                ["Twohundred day average: ", response["twoHundredDayAverage"]],
            ]
            return tabulate(table, tablefmt="mixed_grid")

        table = {
            "Name: ": cls.name(ticker),
            "Current price: ": f"${cls.price(ticker, convert_currency='usd')}",
            "Region: ": response["region"],
            "Language: ": response["language"],
            "Exchange: ": response["fullExchangeName"],
            "Average analyst rating: ": response["averageAnalystRating"],
            "Fifty day average price: ": response["fiftyDayAverage"],
            "Twohundred day average: ": response["twoHundredDayAverage"]
        }
        return table

    @staticmethod
    def remove_suffix(name: str) -> str:
        """Remove the ending suffix like Inc. in Alphabet Inc."""
        suffixes = [
            "corp.",
            ",",
            "co.",
            "ltd.",
            "plc",
            "sa",
            "ag",
            " &",
            "inc.",
            "(the)",
            "ord",
            "sh",
            "inc",
        ]
        # Loop through every suffix and remove it
        for suffix in suffixes:
            name = name.lower().replace(suffix, "")
        return string.capwords(name, sep=None)

    @staticmethod
    def news(ticker: str, timespan=5, index=-1, warning=True) -> str:
        '''get news for a company using the news api'''
        warning = (
                "Warning this feature is not yet fully functional\
 and may not generate a correct article\n\
to disable this warning add the argument warning=False")
        currentdate = datetime.datetime.now()
        timedata = currentdate - datetime.timedelta(days=timespan)
        index += 1
        url_news = (f'https://newsapi.org/v2/everything?'
                    f'q={ticker}&'
                    f'from={timedata.strftime("%Y-%m-%d")}&'
                    f'sortBy=popularity&'
                    f'apiKey={os.environ["NEWS_KEY"]}'
                    )
        response = requests.get(url_news, timeout=10).json()
        # Return the formatted string of the news article
        # try:
        if warning:
            newsformatted = f'{warning}\n\n{response["articles"][index]["title"]} \
                    \n {response["articles"][index]["description"]} \
                    \n Published at {(response["articles"][index]["publishedAt"])[:-10]} by:\
                    {response["articles"][index]["source"]["name"].lstrip()}\
                    \n Read the full article at: {response["articles"][index]["url"]}'
        else:
            newsformatted = f'\n{response["articles"][index]["title"]} \
                    \n {response["articles"][index]["description"]} \
                    \n Published at {(response["articles"][index]["publishedAt"])[:-10]} by:\
                    {response["articles"][index]["source"]["name"].lstrip()}\
                    \n Read the full article at: {response["articles"][index]["url"]}'
        # except KeyError:
        #   newsformatted = "This feature has expired, broken or bugged, please do not use"

        return newsformatted

    @staticmethod
    def converted_currency(price: int, currency) -> int:
        """Convert the price to a different currency using OER."""
        # Acces the workflow defined OER Key using os
        api_key = os.environ["OER_KEY"]
        # Use the OpenExhangeRates api to get current currency rates
        url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
        # Use requests to define as variable
        response = requests.get(url, headers=HEADERS, timeout=10)
        # Check if response was "ok"
        if response.status_code != HTTPStatus.OK:
            raise ConversionError(
                f"[{response.status_code}] - Failed to fetch ticker symbol"
            )
        # Convert to json format so it is indexable
        data = response.json()
        # Index to the location of the uppercase version of the chosen curreny
        try:
            converted_price = data["rates"][currency.upper()] * price
        except LookupError:
            return data
        return round(converted_price, 2)

    @staticmethod
    def request_ticker_info(ticker: str) -> dict:
        """
        Fetch the data for the desired ticker symbol.

        Raises ConversionError if the request wasn't successful.
        """
        response = requests.get(
            API_URL_TEMPLATE.format(ticker=ticker), headers=HEADERS, timeout=10
        )

        if response.status_code != HTTPStatus.OK:
            raise ConversionError(
                f"[{response.status_code}] - Failed to fetch ticker symbol"
            )

        try:
            # Convert to Json format and find price
            data = response.json()["optionChain"]["result"][0]["quote"]
        except IndexError as exc:
            # If price could not be found raise conversionerror
            # This may occur because the ticker is incorrect or non-existand
            raise ConversionError(response.status_code) from exc
        return data

    @classmethod
    def price(cls, ticker: str | list, convert_currency="usd") -> int | dict:
        """
        Get the current price of the stock with the given ticker symbol.

        Raises ConversionError if the ticker symbol is invalid.
        """
        if isinstance(ticker, list):
            price_list = []
            for tick in ticker:
                try:
                    price_list.append(cls.request_ticker_info(tick)["regularMarketPrice"])
                except ConversionError:
                    price_list.append("error")
            return dict(zip(ticker, price_list))

        try:
            price_usd = cls.request_ticker_info(ticker)["regularMarketPrice"]
        except LookupError as exc:
            raise ConversionError(ticker) from exc
        # If user added the convert arg, convert the price to in included currency
        if convert_currency:
            return cls.converted_currency(price_usd, convert_currency)
        return price_usd

    @classmethod
    def name(cls, ticker: str, remove_suffix=False) -> str:
        """
        Get the company name of the stock with the given ticker symbol.

        Raises ConversionError if the ticker symbol is invalid.
        """
        try:
            name = cls.request_ticker_info(ticker)["shortName"]
        except LookupError as exc:
            raise ConversionError(ticker) from exc
        # Check if the name only consist of numbers,
        # and therefore is not what the user is looking for
        if name.isnumeric():
            raise ConversionError(f"{ticker} fetches number instead of str")
        if remove_suffix is not False:
            return cls.remove_suffix(name)
        return name
