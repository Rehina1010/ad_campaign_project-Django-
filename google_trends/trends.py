from pytrends.request import TrendReq


def get_google_trends_data(keyword = "Google Ads"):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([keyword], cat=0, timeframe='now 1-d', geo='', gprop='')

    data = pytrends.interest_over_time()
    return data
