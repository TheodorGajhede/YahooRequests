# Yahoo Requests

A small Python library for getting prices and full names of companies using Yahoo.

[![Github Page](https://img.shields.io/badge/Github-000?logo="github")](https://github.com/TheodorGajhede/YahooRequests/tree/main) 
![Python Versions ](https://img.shields.io/badge/Python-3.7--3.12-259?logo="python") ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/TheodorGajhede/YahooRequests) ![GitHub last commit (branch)](https://img.shields.io/github/last-commit/TheodorGajhede/YahooRequests/main?label=Last%20commit) ![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/TheodorGajhede/YahooRequests/build.yml?style=flat&logo=github&label=Build)![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/TheodorGajhede/YahooRequests/unit_test.yml?style=flat&logo=github&label=Unit%20test)  ![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/TheodorGajhede/YahooRequests/test_publish.yml?style=flat&logo=github&label=Test%20publish)![GitHub](https://img.shields.io/github/license/TheodorGajhede/YahooRequests?label=License)







## Installation

```sh
pip install YahooRequests 
```
## Usage
```python
from YahooRequests import YahooRequests as yr

# Get the live price of Google in USD
price = yr.price("googl")

# Get the full company name of Google
name = yr.name("googl")

# Get the converted price of Google, this only takes currency codes^1 
converted_price = yr.price("googl", "eur")

# Full company name of Google with no suffix, like inc, or corp.
# if no argument is given this will be included
no_suffix_name = yr.name("googl", suffix=False)

# Return simple table with different information
table_company = yr.basic_info("googl")
'''
example:
┍━━━━━━━━━━━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━┑
│ Name:                    │ Alphabet Inc. │
├──────────────────────────┼───────────────┤
│ Current price:           │ $128.86       │
├──────────────────────────┼───────────────┤
│ Region:                  │ US            │
├──────────────────────────┼───────────────┤
│ Language:                │ en-US         │
├──────────────────────────┼───────────────┤
│ Exchange:                │ NasdaqGS      │
├──────────────────────────┼───────────────┤
│ Average analyst rating:  │ 1.9 - Buy     │
├──────────────────────────┼───────────────┤
│ Fifty day average price: │ 123.9172      │
├──────────────────────────┼───────────────┤
│ Twohundred day average:  │ 105.4         │
┕━━━━━━━━━━━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━┙
'''

# Return the most popular news article about a company
# This feature is early acces and might not function properly
# The function will write a warning which can be disable by adding warning=False
news = yr.news("googl")
'''

'''
```

## Footnotes
^1 Currency codes can be found [here](https://www.iban.com/currency-codes)

Average analyst rating explanation: 

If the average rating is close to 5, that means that most analysts rate the stock as a sell. But if the average rating is close to 1, then most analysts have a "buy" or "strong buy" rating. Summary: Analyst ratings are often aggregated into a single score on a scale of 1–5.

### Author

Theodor Gajhede from the northern part of Denmark

## Support

If ```import YahooRequests from YahooRequests``` doesn't work
 try using the "--user" flag when  installing with pip or send a ticket to [RedDied](reddieddk@gmail.com)

## Credits

### Thanks to u/Diapolo10 for helping with version 1.0
