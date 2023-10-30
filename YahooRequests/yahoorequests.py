"""This is a module for extracitng stock data from Yahoo Finance

    An more in-depth guide is in the docs.md file
"""

from http import HTTPStatus
import string
import os
import datetime
from datetime import date
import csv
import requests
from tabulate import tabulate
from newsapi import NewsApiClient


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

    @staticmethod
    def get_api() -> list:
        """
        Returns api names from the api_keys file

        Args:
            None

        Returns:
            A list of all api keys

        Raises:
            N/A
        """
        with open("apikeys.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            apis = []
            line = 1
            for line in reader:
                if reader.line_num == 1:
                    continue  # skip header row
                apis.append(line[1])
            return apis

    @staticmethod
    def remove_suffix(name: str) -> str:
        """
        Removes the suffix (End) of a company name

        Args:
            Name: the name of the company

        Returns:
            The name with all suffixes removed

        Raises:
            N/A
        """
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
    def request_ticker_info(ticker: str) -> dict:
        """
        The request script for most data used here

        Args:
            ticker: The ticker symbol of the stock.

        Returns:
            The requests data (A big dict with one hell lot of data)

        Raises:
            ConversionError: If the ticker is not Converted correctly and an exception is raised from the requests script
            If price could not be found raise conversionerror This may occur because the ticker is incorrect or non-existand
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
    def converted_currency(cls, price: int, currency) -> float:
        """
        Converts an price in dollars to another currency

        Args:
            price: The price of the stock
            currency: The currency to convert the price to

        Returns:
            The converted price as an interger

        Raises:
            ConversionError:
                If the ticker is not Converted correctly and an exception is raised from the requests script
            LookupError: Occurs if the dict does not have the desired data.
        """
        api_key = cls.get_api()[1]
        if not api_key[1].isnumeric():
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

    @classmethod
    def news(cls, ticker: str, index=-1, warning=True) -> str:
        """
        Returns a string of news about a company

        Args:
            ticker: The ticker symbol of the stock.
            Timespan: the timespan the script will search for the data in
                An interger representing number of days to search in
            Index: The number article, -1 will be the first and 0 will be the second and etc.
            Warning: By default it will write an error because this is still in beta

        Returns:
            A news segment about a company

        Raises:
            ConversionError:
                If the ticker is not Converted correctly and an exception is raised from the requests script
        """
        warning_text = """
        Warning this feature is not yet fully functional
        and may not generate a correct article.
        To disable this warning add the argument warning=False.
        """
        # Initialize
        api_key = cls.get_api()[0]
        if not api_key[0].isnumeric():
            # Acces the workflow defined OER Key using os
            api_key = os.environ["NEWS_KEY"]
        newsapi = NewsApiClient(api_key=api_key)
        index += 1
        # Return the formatted string of the news article
        response = newsapi.get_top_headlines(
                q=(cls.name(ticker)),
                category='business',
                language='en',
                country='us'
                )
        # If there are no articles to use use the get_everything method instead
        if response == {'status': 'ok', 'totalResults': 0, 'articles': []}:
            today = date.today()
            response = newsapi.get_everything(q=ticker,
                                              from_param=today - datetime.timedelta(days=5),
                                              to=today,
                                              language='en',
                                              sort_by='relevancy',
                                              )

        try:
            newsformatted = f'\n{response["articles"][index]["title"]} \
                    \n {response["articles"][index]["description"]} \
                    \n Published at {(response["articles"][index]["publishedAt"])[:-10]} by:\
                    {response["articles"][index]["source"]["name"].lstrip()}\
                    \n Read the full article at: {response["articles"][index]["url"]}'
        except (KeyError, IndexError):
            newsformatted = (
                "This feature has expired, broken or bugged, please do not use", response
            )
        if warning:
            return warning_text + str(newsformatted)
        return str(newsformatted)

    @classmethod
    def get_history(cls, ticker: str, start: datetime.date | str, end: datetime.date | str, interval="1d") -> list:

        """
        Retrive daily prices of a stock from end- and startdate

        Args:
            ticker: The ticker symbol of the stock.
            start: The start date of the date range. Can be a datetime.date object or a string in the format "YYYY-MM-DD".
            end: The end date of the date range. Can be a datetime.date object or a string in the format "YYYY-MM-DD".
            interval: The interval between the price points
                '1d', '5d', '1wk', '1mo', '3mo', '1d', '5d', '1mo', '3mo'
                no other intervals will be accepted
        Returns:
            A list of prices from every day of the open market in the time period

        Raises:
            TypeError: If the ticker is not a string or if the start and end dates are not valid datetime objects.
            TypeError: If the start date is after the end date.
            ConnectionError: If the connection to Yahoo Finance fails.
            JSONDecodeError: If the JSON data returned by Yahoo Finance is invalid.
        """

        try:
            # Connvert values to datetime type
            if isinstance(start, datetime.date):
                start = start.strftime("%Y-%m-%d")
            if isinstance(end, datetime.date):
                end = end.strftime("%Y-%m-%d")
            # If all values are of the correct type conntinue
            unix_start = int(datetime.datetime.strptime(start, "%Y-%m-%d").timestamp())
            unix_end = int(datetime.datetime.strptime(end, "%Y-%m-%d").timestamp())
            valid_intervals = '1d', '5d', '1wk', '1mo', '3mo', '1d', '5d', '1mo', '3mo'
            # Check if the interval is valid
            if interval not in valid_intervals:
                raise ConversionError(
                    f"[{interval} is not a valid intervals all valid intervals are: {valid_intervals}]"
                )
            # If start is after end, raise a error
            if unix_end < unix_start:
                raise TypeError(
                    f"Error Start date cannnot be after the end date. startDate = {start} endDate = {end}"
                )
            # This link will look kinda funky because i am stupid
            link = f"https://query1.finance.yahoo.com/v7/finance/chart/{ticker}?period1={unix_start}&period2={unix_end}&interval={interval}"
            # Make the request to Yahoo Finance
            response = requests.get(link, timeout=10, headers=HEADERS)
            # Check the status code of the response
            if response.status_code != HTTPStatus.OK:
                raise ConversionError(
                    f"[{response.status_code}] - Failed to fetch ticker symbol"
                )
            # Parse the JSON response
            data = response.json()
            # Extract the list of price values
            try:
                data["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"]
            except IndexError as exc:
                # If price could not be found raise conversionerror
                # This may occur because the ticker is incorrect or non-existand
                raise ConversionError(response.status_code) from exc
            return data
        except (ValueError, TypeError, ConnectionError) as error:
            raise ConversionError(
                f"Error check the data and the formatting, Error Caught: {error}"
            ) from error

    @classmethod
    def average_price(cls, ticker: str, start: datetime.date | str, end: datetime.date | str, interval="1d") -> float:
        """
        Calculate the average price of a stock from a start date and end date.

        Args:
            ticker: The ticker symbol of the stock.
            start: The start date of the date range. Can be a datetime.date object or a string in the format "YYYY-MM-DD".
            end: The end date of the date range. Can be a datetime.date object or a string in the format "YYYY-MM-DD".

        Returns:
            The average price of a stock in the designated time period.

        Raises:
            Internal exceptions from the get_history:
                TypeError: If the ticker is not a string or if the start and end dates are not valid datetime objects.
                TypeError: If the start date is after the end date.
                ConnectionError: If the connection to Yahoo Finance fails.
                JSONDecodeError: If the JSON data returned by Yahoo Finance is invalid.
        """
        data = cls.get_history(ticker, start, end, interval)
        # Index to the correct data in the requested data
        lst = data["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"]  # type: ignore
        # Return the average value of all
        return round(sum(lst) / len(lst), 2)

    @classmethod
    def basic_info(cls, ticker: str, dictionary=False) -> str | dict:
        """
        Returns the a small table of data for a company

        Args:
            ticker: The ticker symbol of the stock.
            dictionary:
                The boolean representing if the returned value should be formatted as a dictionary or tabulate

        Returns:
            A tabluate or dictionry of information about a company

        Raises:
            ConversionError:
                If the ticker is not Converted correctly and an exception is raised from the requests script
        """
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
            "Average analyst rating: ": cls.rating(ticker),
            "Fifty day average price: ": response["fiftyDayAverage"],
            "Twohundred day average: ": response["twoHundredDayAverage"],
        }
        return table

    @classmethod
    def rating(cls, ticker: str) -> int:
        """
        Returns the current price of one or more tickers, in different currencies

        Args:
            ticker: The ticker symbol of the stock.

        Returns:
            an interger representing the average analyst rating of a stock

        Raises:
            ConversionError:
                If the ticker is not Converted correctly and an exception is raised from the requests script
        """
        response = cls.request_ticker_info(ticker)
        return response["averageAnalystRating"]

    @classmethod
    def price(cls, ticker: str | list, convert_currency=None) -> float | dict:
        """
        Returns the current price of one or more tickers, in different currencies

        Args:
            ticker: The ticker symbol of the stock.
            convert_currency: The str deciding what currency to convert the price to.

        Returns:
            The price of a ticker as a int, if there are more than one ticker, it will be a dict

        Raises:
            ConversionError:
                If the ticker is not Converted correctly and an exception is raised from the requests script
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
        Returns the name of a company from the ticker, also includes removing the suffix

        Args:
            ticker: The ticker symbol of the stock.
            remove_suffix: Boolean deciding for the removal of the suffix e.g. Corp. Inc.

        Returns:
            The full name of a company

        Raises:
            ConversionError: if there is an error when getting the full name
            ConversionError: If the ticker is converted and the returned value is numeric
        """
        try:
            name = cls.request_ticker_info(ticker)["shortName"]
        except LookupError as exc:
            raise ConversionError(ticker) from exc
        # Check if the name only consist of numbers,
        # and therefore is not what the user is looking for
        if name.isnumeric():
            raise ConversionError(f"{ticker} fetches number instead of str")
        # Return a version of the code with the suffix removed
        if remove_suffix is not False:
            return cls.remove_suffix(name)
        return name
