# Yahoo Requests

A small Python library for getting prices and full names of companies using Yahoo.

## Author

Theodor Gajhede from the north of Denmark

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
```

## Installation

```python
pip install YahooRequests 
```
## Footnotes
^1 Currency codes can be found [here](https://www.iban.com/currency-codes)

## Support

If ```import YahooRequests from YahooRequests``` doesn't work
 try using the "--user" flag when  installing with pip or send a ticket to [RedDied](reddieddk@gmail.com)

## Credits

### Thanks to u/Diapolo10 for helping with version 1.0
