from binance.client import Client
import requests, json, time

with open('/root/binance_strategies/api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

while True:
    try:

        with open('/root/binance_strategies/variables.json') as v:
            variables = json.load(v)

        time_to_cool_down = variables['time_to_cool_down']
        multiplier = variables['multiplier']

        symbol = 'ETHBUSD'
        quantityPrecision = 3
        minNotional = 0.003 * 10
        quantity = round(minNotional * multiplier, quantityPrecision)

        liquidations_in_USD = variables['liquidations_in_USD']

        headers = {'coinglassSecret': '50f90ddcd6a8437992431ab0f1b698c1'}
        url = requests.get(
            "https://open-api.coinglass.com/api/pro/v1/futures/liquidation/detail/chart?symbol=ETH&timeType=3",
            headers=headers)
        text = url.text
        data = json.loads(text)

        long_signal = float(data['data'][89]['buyVolUsd'])
        if long_signal > liquidations_in_USD:
            client.futures_create_order(symbol=symbol,
                                        side='BUY',
                                        positionSide='LONG',
                                        type='MARKET',
                                        quantity=quantity)
            time.sleep(time_to_cool_down / 10)

        short_signal = float(data['data'][89]['sellVolUsd'])
        if short_signal > liquidations_in_USD:
            client.futures_create_order(symbol=symbol,
                                        side='SELL',
                                        positionSide='SHORT',
                                        type='MARKET',
                                        quantity=quantity)
            time.sleep(time_to_cool_down / 10)

    except Exception as e:
        print("Function errored out!", e)
        print("Retrying ... ")
