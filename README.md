# Yahoo Requests - Python Library for Company Data Retrieval

Welcome to Yahoo Requests, a Python library designed to facilitate the retrieval of company information such as prices and full names using Yahoo's data sources.

[![Github Page](https://img.shields.io/badge/Github-000?logo=github)](https://github.com/TheodorGajhede/YahooRequests/tree/main) 
![Python Versions](https://img.shields.io/badge/Python-3.7--3.12-259?logo=python) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/TheodorGajhede/YahooRequests) ![GitHub last commit (branch)](https://img.shields.io/github/last-commit/TheodorGajhede/YahooRequests/main?label=Last%20commit) ![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/TheodorGajhede/YahooRequests/build.yml?style=flat&logo=github&label=Build)![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/TheodorGajhede/YahooRequests/unit_test.yml?style=flat&logo=github&label=Unit%20test)  ![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/TheodorGajhede/YahooRequests/test_publish.yml?style=flat&logo=github&label=Test%20publish)![GitHub](https://img.shields.io/github/license/TheodorGajhede/YahooRequests?label=License)

## Features

Retrieve live prices, full names, and converted prices of companies (supports currency codes)
Get the most popular news article about a company (early access feature)
Calculate the average price of a stock in a time period
Return a simple table with different information about the company
Easy to use and install

## Installation

To use Yahoo Requests, you can easily install it using pip:

```sh
pip install YahooRequests 
```
## Usage
Here's how you can use Yahoo Requests to retrieve company data in Python:
```python
from YahooRequests import YahooRequests as yr

# Get the live price of Google in USD
price = yr.price("googl")

# Get the full company name of Google
name = yr.name("googl")

# Get the converted price of Google (supports currency codes)
converted_price = yr.price("googl", "eur")

# Full company name of Google with no suffix (like inc or corp)
# If no argument is given, this will be included
no_suffix_name = yr.name("googl", suffix=False)

# Return a simple table with different information about the company
table_company = yr.basic_info("googl")

# Return the most popular news article about a company (Early access feature)
news = yr.news("googl", timespan=5, warning=True)

# Return the average price of a stock in a time period
average_price = yr.average_price("aapl", "2021-1-1", "2022-1-1")
```

## Footnotes
Currency codes can be found [Here](https://www.iban.com/currency-codes).

Average analyst rating explanation:

- *If the average rating is close to 5, that means most analysts rate the stock as a sell.
 Conversely, if the average rating is close to 1, most analysts have a "buy" or "strong buy" rating.
In summary, analyst ratings are often aggregated into a single score on a scale of 1–5.*

## Author
Theodor Gajhede from the northern part of Denmark.

## Support
 If you encounter issues with the library, try using the "--user" flag when installing with pip or send a support ticket to RedDied at reddied@gmail.com.

### Credits
 Special thanks to u/Diapolo10 for their contribution to version 1.0.