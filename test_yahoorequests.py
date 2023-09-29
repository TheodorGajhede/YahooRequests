'''
This is tests
'''

from YahooRequests import YahooRequests


def test_price():
    '''Test the method for getting price'''
    assert isinstance(YahooRequests.price("googl"), float)
    assert isinstance(YahooRequests.price("aapl"), float)
    test_list = ["aapl", "googl", "pi", "plug"]
    assert isinstance(YahooRequests.price(test_list), dict)


def test_name():
    '''Test the name method with no args'''
    assert YahooRequests.name("googl") == "Alphabet Inc."
    assert YahooRequests.name("aapl") == "Apple Inc."


def test_convert():
    '''Test the method for conveting currency with api'''
    assert isinstance(YahooRequests.converted_currency(100, "dkk"), float)
    assert YahooRequests.converted_currency(100, "eur") >= 0


def test_suffix():
    '''Test the method for removing the suffix from a company name'''
    assert YahooRequests.remove_suffix("Apple Inc.") == "Apple"
    assert YahooRequests.remove_suffix("Google, Inc") == "Google"
    assert YahooRequests.remove_suffix("Company Co.") == "Company"


def test_basic_info():
    '''Test the method for priting a table of basic info'''
    assert isinstance(YahooRequests.basic_info("aapl"), str)
    assert isinstance(YahooRequests.basic_info("aapl", dictionary=True), dict)


def test_news():
    '''Test the method and api for getting news'''
    assert isinstance(YahooRequests.news("googl"), str)
    assert YahooRequests.news("googl") is not YahooRequests.news("googl", warning=False)
