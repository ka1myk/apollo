import json
from telegram_exception_alerts import Alerter
import hmac
import time
import hashlib
import requests
from urllib.parse import urlencode

with open('variables.json') as v:
    variables = json.load(v)

bot_token = variables['telegram']['bot_token']
bot_chatID = variables['telegram']['bot_chatID']
tg_alert = Alerter(bot_token=bot_token, chat_id=bot_chatID)

KEY = variables['binance_01']['key']
SECRET = variables['binance_01']['secret']
BASE_URL = "https://eapi.binance.com"  # production base url

""" ======  begin of functions, you don't need to touch ====== """


def hashing(query_string):
    return hmac.new(
        SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()


def get_timestamp():
    return int(time.time() * 1000)


def dispatch_request(http_method):
    session = requests.Session()
    session.headers.update(
        {"Content-Type": "application/json;charset=utf-8", "X-MBX-APIKEY": KEY}
    )
    return {
        "GET": session.get,
        "DELETE": session.delete,
        "PUT": session.put,
        "POST": session.post,
    }.get(http_method, "GET")


# used for sending request requires the signature
def send_signed_request(http_method, url_path, payload={}):
    query_string = urlencode(payload, True)
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp())
    else:
        query_string = "timestamp={}".format(get_timestamp())

    url = (
            BASE_URL + url_path + "?" + query_string + "&signature=" + hashing(query_string)
    )
    print("{} {}".format(http_method, url))
    params = {"url": url, "params": {}}
    response = dispatch_request(http_method)(**params)
    return response.json()


# used for sending public data request
def send_public_request(url_path, payload={}):
    query_string = urlencode(payload, True)
    url = BASE_URL + url_path
    if query_string:
        url = url + "?" + query_string
    print("{}".format(url))
    response = dispatch_request("GET")(url=url)
    return response.json()


""" ======  end of functions ====== """


### USER_DATA endpoints, call send_signed_request #####
# get account informtion
# if you can see the account details, then the API key/secret is correct
# response = send_signed_request("GET", "/api/v3/account")
# print(response)


# New Future Account Transfer (FUTURES)
# params = {"asset": "USDT", "amount": 0.01, "type": 1}
# response = send_signed_request("POST", "/sapi/v1/futures/transfer", params)
# print(response)


@tg_alert
def user_trades():
    params = {"symbol": "ETH-221230-4500-C"}
    response = send_signed_request("GET", "/eapi/v1/trades", params)
    print(response)


user_trades()
