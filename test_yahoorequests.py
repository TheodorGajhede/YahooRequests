from YahooRequests import YahooRequests as yr

def test_price():
    assert type(yr.price("googl")) == float
    assert type(yr.price("aapl")) == float
   

def test_name():
    assert yr.name("googl") == "Alphabet Inc."
    assert yr.name("aapl") == "Apple Inc."


def test_convert():
    assert type(yr.converted_currency(100, "dkk")) == float
    assert yr.converted_currency(100, "eur") >= 0


def test_suffix():
    assert yr.remove_suffix("Apple Inc.") == "Apple"
    assert yr.remove_suffix("Google, Inc") == "Google"
    assert yr.remove_suffix("Company Co.") == "Company"