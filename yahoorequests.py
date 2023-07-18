import requests

'''If you are one day trying to use this code and it does not work
    it is up to god and you to fix it, becuase OC doesn't know what he is doing
            - OC'''


class ConvertError(Exception):
    "Ticker could not be converted to companmy name please contact the creater"
    pass


class YahooRequest():
    global url
    global headers

    # Define url for requesting data
    url = 'https://query1.finance.yahoo.com/v7/finance/options/{}'

    # Yahoo's api was shut down in 2017 so making a headers is required to look like a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)\
        AppleWebKit/537.36 (KHTML, like Gecko)\
        Chrome/108.0.0.0 Safari/537.36'
        }

    @staticmethod
    def price(ticker) -> int:
        # Request url formatted as if the ticker is a str including headers for baiting as if a browser
        response = requests.get(url.format(*ticker), headers=headers)
        if response.statuscode == 200:
            # Unpack the data as a json type
            data = response.json()
            # return only the needed data
            return data["optionChain"]["result"][0]["quote"]["regularMarketPrice"]
        else:
            # raise the custom convert error if the url could not be reached
            # or any other error is raised when requesting
            raise ConvertError

    @staticmethod
    def name(ticker) -> str:
        # Request url formatted as if the ticker is a str including headers for baiting as if a browser
        response = requests.get(url.format(*ticker), headers=headers)
        if response.status_code == 200:
            # Unpack the data as a json type
            data = response.json()
            # return only the needed data
            return data["optionChain"]["result"][0]["quote"]["shortName"]
        else:
            # raise the custom ConvertError
            raise ConvertError()
