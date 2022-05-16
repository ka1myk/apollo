import json
from decimal import Decimal

from tradingview_ta import TA_Handler, Interval, Exchange
from variables import time_to_create_order, time_to_wait_one_more_check, time_to_cool_down, time_to_create_gs_order
import time
from binance.client import Client

with open('/root/passivbot/api-keys.json') as p:
    creds = json.load(p)

client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

FTTBUSDPERP_INTERVAL_1_MINUTE = TA_Handler(
    symbol="FTTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)

FTTBUSDPERP_INTERVAL_5_MINUTES = TA_Handler(
    symbol="FTTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES
)

FTTBUSDPERP_INTERVAL_15_MINUTES = TA_Handler(
    symbol="FTTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_15_MINUTES
)

FTTBUSDPERP_INTERVAL_30_MINUTES = TA_Handler(
    symbol="FTTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_30_MINUTES
)

FTTBUSDPERP_INTERVAL_1_HOUR = TA_Handler(
    symbol="FTTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_HOUR
)

FTTBUSDPERP_INTERVAL_2_HOURS = TA_Handler(
    symbol="FTTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_2_HOURS
)

FTTBUSDPERP_INTERVAL_4_HOURS = TA_Handler(
    symbol="FTTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_4_HOURS
)

FTTBUSDPERP_INTERVAL_1_DAY = TA_Handler(
    symbol="FTTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_DAY
)

while True:
    try:
        if (
                FTTBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and FTTBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and FTTBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and FTTBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and FTTBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
        ):
            time.sleep(time_to_wait_one_more_check)

            if (
                    FTTBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY", "BUY")
                    and FTTBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY", "BUY")
                    and FTTBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY", "BUY")
                    and FTTBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY", "BUY")
                    and FTTBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY", "BUY")
            ):
                # open long order and close long order#
                price = format(Decimal(client.futures_coin_ticker(symbol='FTTUSD_PERP')[0]['lastPrice']), '.4f')
                client.futures_create_order(symbol='FTTBUSD', side='BUY', positionSide='LONG', type='LIMIT',
                                            quantity=0.2,
                                            timeInForce='GTC', price=price)
                time.sleep(1)

                priceForCloseLongOrder = format(
                    Decimal(client.futures_position_information(symbol='FTTBUSD')[1]['entryPrice']), '.4f')
                amtForCloseLongOrder = Decimal(client.futures_position_information(symbol='FTTBUSD')[1]['positionAmt'])

                print(priceForCloseLongOrder)
                print(amtForCloseLongOrder)

                client.futures_create_order(symbol='FTTBUSD', side='SELL', positionSide='LONG', type='LIMIT',
                                            quantity=amtForCloseLongOrder,
                                            timeInForce='GTX', price=priceForCloseLongOrder)
                # -----------------------------------#

                time.sleep(time_to_cool_down)

        if (
                FTTBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and FTTBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and FTTBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and FTTBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and FTTBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
        ):
            time.sleep(time_to_wait_one_more_check)

            if (
                    FTTBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL", "SELL")
                    and FTTBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL", "SELL")
                    and FTTBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL", "SELL")
                    and FTTBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL", "SELL")
                    and FTTBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL", "SELL")
            ):
                # open short order and close short order#
                price = format(Decimal(client.futures_coin_ticker(symbol='FTTUSD_PERP')[0]['lastPrice']), '.4f')
                client.futures_create_order(symbol='FTTBUSD', side='SELL', positionSide='SHORT', type='LIMIT',
                                            quantity=0.2,
                                            timeInForce='GTC', price=price)
                time.sleep(1)

                priceForCloseLongOrder = format(
                    Decimal(client.futures_position_information(symbol='FTTBUSD')[2]['entryPrice']), '.4f')
                amtForCloseLongOrder = format(
                    abs(Decimal(client.futures_position_information(symbol='FTTBUSD')[2]['positionAmt'])))

                print(priceForCloseLongOrder)
                print(amtForCloseLongOrder)

                client.futures_create_order(symbol='FTTBUSD', side='BUY', positionSide='SHORT', type='LIMIT',
                                            quantity=amtForCloseLongOrder,
                                            timeInForce='GTX', price=priceForCloseLongOrder)
                # -----------------------------------#

                time.sleep(time_to_cool_down)

    except Exception as e:
        print("Function errored out!", e)
        print("Retrying ... ")
