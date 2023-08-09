# Yahoo Requests

A small Python library for getting prices and full names of companies using Yahoo.

## Author

Theodor Gajhede from the north of Denmark

## Usage

```python
from YahooRequests import YahooRequests as yr

# Get the live price of Google
price = yr.price("googl")

# Get the full company name of Google
name = yr.name("googl")
```

## Installation

```python
pip install YahooRequests 
```

## Support

If ```import YahooRequests from YahooRequests``` doesn't work
 try using the "--user" flag when  installing with pip or send a ticket to [RedDied](reddieddk@gmail.com)

## Credits

### Thanks to u/Diapolo10 for helping with version 1.0
