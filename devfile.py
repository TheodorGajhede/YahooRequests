from YahooRequests import YahooRequests
import json
succesfull = []
intevals = "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"
for interval in intevals:
    try:
        history = YahooRequests.get_history("pi", "2022-10-23", "2023-10-23", interval=interval)
        data = history["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"]
        succesfull.append(interval)
    except Exception:
        print("error at: ", interval)
print(intevals)

intervals = "1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"
for interval in intervals:
    try:
        history = YahooRequests.get_history("pi", "2022-10-23", "2023-10-23", interval=interval)
        data = history["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"]
        print(interval)
        succesfull.append(interval)
    except Exception:
        print("error at: ", interval)
print(intervals)
print(succesfull)