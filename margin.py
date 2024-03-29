import json
import secrets

from binance.client import Client
from binance.helpers import round_step_size

from telegram_exception_alerts import Alerter

with open('/root/apollo/variables.json') as v:
    variables = json.load(v)

client = Client(variables['binance_01']['key'], variables['binance_01']['secret'])
tg_alert = Alerter(bot_token=variables['telegram']['bot_token'], chat_id=variables['telegram']['bot_chatID'])


def get_random_tradeable_pair_on_margin():
    temp = []
    for y in client.get_margin_all_pairs():
        if y["base"] in variables['coin'] and y["quote"] in variables['coin'] and y["isMarginTrade"] is True and y[
            "base"] not in temp:
            temp.append(y["symbol"])
    margin_tradeable_pairs = list(dict.fromkeys(temp))
    return secrets.choice(margin_tradeable_pairs)


symbol = get_random_tradeable_pair_on_margin()
symbol_info = client.get_symbol_info(symbol)


def get_fees():
    return float(client.get_trade_fee(symbol=symbol)[0]["makerCommission"]) + float(
        client.get_trade_fee(symbol=symbol)[0]["takerCommission"])


def set_greed():
    if float(client.get_margin_account()['totalAssetOfBtc']) * float(
            client.get_avg_price(symbol="BTCBUSD")['price']) < variables['budget_up_to_1_greed']:
        greed = variables['greed']
    else:
        greed = float(client.get_margin_account()['totalAssetOfBtc']) * float(
            client.get_avg_price(symbol="BTCBUSD")['price']) / variables['budget_up_to_1_greed']
    return greed


def get_min_notional():
    for y in symbol_info['filters']:
        if y['filterType'] == 'MIN_NOTIONAL':
            return y['minNotional']


def get_tick_size():
    for y in symbol_info['filters']:
        if y['filterType'] == 'PRICE_FILTER':
            return y['tickSize']


def get_lot_size():
    for x in symbol_info["filters"]:
        if x['filterType'] == 'LOT_SIZE':
            return x['stepSize']


def margin_create_market_buy():
    client.create_margin_order(symbol=symbol,
                               quoteOrderQty=round_step_size(float(get_min_notional()) * set_greed(), get_tick_size()),
                               side='BUY',
                               type='MARKET'
                               )


def margin_create_market_sell():
    client.create_margin_order(symbol=symbol,
                               quoteOrderQty=round_step_size(float(get_min_notional()) * set_greed(), get_tick_size()),
                               side='SELL',
                               type='MARKET'
                               )


def margin_create_limit_sell():
    client.create_margin_order(symbol=symbol,
                               quantity=client.get_all_margin_orders(symbol=symbol, limit=1)[0]["origQty"],
                               price=round_step_size(
                                   float(client.get_avg_price(symbol=symbol)['price']) * float(
                                       secrets.choice(variables['margin_sell_profit']) + get_fees()),
                                   get_tick_size()),
                               side='SELL',
                               type='LIMIT',
                               timeInForce="GTC"
                               )


def margin_create_limit_buy():
    client.create_margin_order(symbol=symbol,
                               quantity=client.get_all_margin_orders(symbol=symbol, limit=1)[0]["origQty"],
                               price=round_step_size(
                                   float(client.get_avg_price(symbol=symbol)['price']) * float(
                                       secrets.choice(variables['margin_buy_profit']) - get_fees()),
                                   get_tick_size()),
                               side='BUY',
                               type='LIMIT',
                               timeInForce="GTC"
                               )


@tg_alert
def go_baby_margin():
    if secrets.randbelow(2) == 1:
        margin_create_market_buy()
        margin_create_limit_sell()
    else:
        margin_create_market_sell()
        margin_create_limit_buy()


go_baby_margin()
