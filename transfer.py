from helper import *


def transfer_free_USD_to_spot():
    for x in client.futures_account_balance():
        matchObj = re.search("^((?!USD).)*$", x["asset"])
        if not matchObj and float(x["withdrawAvailable"]) > 0:
            try:
                client.futures_account_transfer(asset=x["asset"],
                                                amount=float(x["withdrawAvailable"]),
                                                type=2,
                                                timestamp=serverTime)
            except:
                print("fail transfer", x["asset"], "to spot")


def usdt_to_busd_on_spot():
    if float(client.get_asset_balance(asset='USDT')['free']) > 10:
        try:
            client.create_order(symbol="BUSDUSDT",
                                side='BUY',
                                type='MARKET',
                                quoteOrderQty=round(float(client.get_asset_balance(asset='USDT')['free'])))

            dust_to_bnb()

        except:
            print("fail to convert USDT to BUSD")


def dust_to_bnb():
    try:
        client.transfer_dust(asset="USDT")
    except:
        print("fail to dust USDT to BNB")


def buy_coins_on_spot():
    if float(client.get_asset_balance(asset='BUSD')['free']) > 10:
        try:
            client.create_order(symbol="BTCBUSD",
                                side='BUY',
                                type='MARKET',
                                quoteOrderQty=float(client.get_asset_balance(asset='BUSD')['free']))
        except:
            print("fail to buy BTC for BUSD")


def transfer_free_spot_coin_to_futures():
    for x in client.futures_account_balance():
        matchObj = re.search("^((?!USD).)*$", x["asset"])
        if matchObj and float(client.get_asset_balance(asset=x["asset"])["free"]) > 0:
            try:
                client.futures_account_transfer(asset=x["asset"],
                                                amount=float(client.get_asset_balance(asset=x["asset"])["free"]),
                                                type=1,
                                                timestamp=serverTime)
            except:
                print("fail transfer", x["asset"], "to futures")


def to_the_moon_and_back():
    try:
        transfer_free_USD_to_spot()
        usdt_to_busd_on_spot()
        buy_coins_on_spot()
        transfer_free_spot_coin_to_futures()
    except:
        print("may the Force be with you")


to_the_moon_and_back()