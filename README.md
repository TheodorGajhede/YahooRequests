# Yahoo Requests

## By Theodor Gajhede from the northeren part of Denmark

### This is a small library for getting prices and fullnames of companies using Yahoo

### How to use

    from YahooRequests import YahooRequests as yr    
    # Now you can just print this value or assign it as a variable
    yr.price("googl")
    # The same goes for name
    yr.name("googl")

### YahooRequests.price(ticker)

    It is very simple you are only required to input a ticker  and it will return the live price
    the ticker will be unpacked using * so it can be a str, or a single byte list like ["googl"]

### YahooRequests.convert(ticker)

    The same goes for convert, the returned value will be the full company name
