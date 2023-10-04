## This module for extracting stock data from Yahoo Finance

This module provides a number of functions for extracting stock data from Yahoo Finance. The data that can be extracted includes:

* Basic information about a company, such as its name, current price, region, language, exchange, average analyst rating, fifty day average price, and two-hundred day average price.
* News articles about a company.
* The current price of a stock, in USD or converted to another currency.
* The company name of a stock.

### Usage

The module can be used as follows:

```python
import YahooRequests as yr

# Get the basic information about a company
ticker = "AAPL"
basic_info = yr.basic_info(ticker)

# Get news articles about a company
ticker = "AAPL"
news = yr.news(ticker)

# Get the current price of a stock, in USD
ticker = "AAPL"
price = yr.price(ticker)

# Get the current price of a stock, converted to EUR
ticker = "AAPL"
price_eur = yr.price(ticker, convert_currency="eur")

# Get the company name of a stock
ticker = "AAPL"
company_name = yr.name(ticker)

# Get the average analyst rating of a stock
ticker = "AAPL"
average_analyst_rating = yr.rating(ticker)
```

### Example

The following example shows how to use the module to get the basic information about Apple and print it to the console:


```python
import YahooRequests as yr

# Get the basic information about Apple
ticker = "AAPL"
basic_info = yr.basic_info(ticker)

# Print the basic information to the console
print(basic_info)
```
Output:
```python
[
    ["Name:", "Apple Inc."],
    ["Current price:", "$150.00"],
    ["Region:", "United States"],
    ["Language:", "English"],
    ["Exchange:", "Nasdaq"],
    ["Average analyst rating:", "Strong Buy"],
    ["Fifty day average price:", "$145.00"],
    ["Twohundred day average price:""$130.00"]
]
```


### Documentation for individual functions

The following is more detailed documentation for each of the functions in the module:

#### `basic_info()`

The `basic_info()` function returns a dictionary of basic information about a company, such as its name, current price, region, language, exchange, average analyst rating, fifty day average price, and two-hundred day average price.

**Parameters:**

* `ticker`: The ticker symbol of the company.

**Returns:**

A dictionary of basic information about the company.

#### `news()`

The `news()` function returns a list of news articles about a company.

**Parameters:**

* `ticker`: The ticker symbol of the company.
* `timespan`: The number of days to go back in time to get news articles for. (Default: 5)
* `index`: The index of the news article to return. (Default: -1, which returns the most recent article)
* `warning`: Whether to show a warning message that the news feature is not yet fully functional. (Default: True)

**Returns:**

A list of news articles about the company.

#### `price()`

The `price()` function returns the current price of a stock, in USD or converted to another currency.

**Parameters:**

* `ticker`: The ticker symbol of the company.
* `convert_currency`: The currency to convert the price to. (Default: "usd")

**Returns:**

The current price of the stock, in the specified currency.

#### `name()`

The `name()` function returns the company name of a stock.

**Parameters:**

* `ticker`: The ticker symbol of the company.
* `remove_suffix`: Whether to remove common suffixes from the company name, such as "Inc." or "Corp.". (Default: False)

**Returns:**

The company name of the stock.

#### `rating()`

The `rating()` function returns a average analyst rating of a stock

**Parameters:**

* `ticker`: The ticker symbol of the company.

**Returns:**

An integer representing the average analyst rating

#### `average_price()`

The `average_price()` function returns the average price of a stock in a time period

**Parameters**

* ticker: The ticker symbol of the stock.
* start: The start date of the date range. Can be a datetime.date object or a string in the format "YYYY-MM-DD".
* end: The end date of the date range. Can be a datetime.date object or a string in the format "YYYY-MM-DD".
* Interval: The interval between the price snippets the interval must be "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo" all others will raise an error

**Returns**

The average price of the stock for the given date range.

### Additional notes

Please note that the Yahoo Finance API has been shut down, so this module uses a workaround to make it appear to be a browser in order to fetch data. This workaround may not work in the future.

Also, please note that the news feature is not yet fully functional and may not generate a correct article