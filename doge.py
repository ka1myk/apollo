import json
from decimal import Decimal

from tradingview_ta import TA_Handler, Interval, Exchange
from variables import time_to_create_order, time_to_wait_one_more_check, time_to_cool_down, time_to_create_gs_order
import time
from binance.client import Client

with open('/root/passivbot/api-keys.json') as p:
    creds = json.load(p)

client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

DOGEBUSDPERP_INTERVAL_1_MINUTE = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)

DOGEBUSDPERP_INTERVAL_5_MINUTES = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES
)

DOGEBUSDPERP_INTERVAL_15_MINUTES = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_15_MINUTES
)

DOGEBUSDPERP_INTERVAL_30_MINUTES = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_30_MINUTES
)

DOGEBUSDPERP_INTERVAL_1_HOUR = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_HOUR
)

DOGEBUSDPERP_INTERVAL_2_HOURS = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_2_HOURS
)

DOGEBUSDPERP_INTERVAL_4_HOURS = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_4_HOURS
)

DOGEBUSDPERP_INTERVAL_1_DAY = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_DAY
)

while True:
    try:
        if (
                DOGEBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and DOGEBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and DOGEBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and DOGEBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and DOGEBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
        ):
            time.sleep(time_to_wait_one_more_check)

            if (
                    DOGEBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY", "BUY")
                    and DOGEBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY", "BUY")
                    and DOGEBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY", "BUY")
                    and DOGEBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY", "BUY")
                    and DOGEBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY", "BUY")
            ):
                # open long order and close long order#
                priceForOpenLongOrder   = format(Decimal(client.futures_coin_ticker(symbol='DOGEUSD_PERP')[0]['lastPrice']), '.5f')
                client.futures_create_order(symbol='DOGEBUSD', side='BUY', positionSide='LONG', type='LIMIT',
                                            quantity=60,
                                            timeInForce='GTX', price=priceForOpenLongOrder)
                time.sleep(1)

                priceForCloseLongOrder = format(
                    Decimal(client.futures_position_information(symbol='DOGEBUSD')[1]['entryPrice']), '.5f')
                amtForCloseLongOrder = Decimal(client.futures_position_information(symbol='DOGEBUSD')[1]['positionAmt'])

                print("priceForCloseLongOrder", priceForCloseLongOrder)
                print("amtForCloseLongOrder", amtForCloseLongOrder)

                client.futures_create_order(symbol='DOGEBUSD', side='SELL', positionSide='LONG', type='LIMIT',
                                            quantity=amtForCloseLongOrder,
                                            timeInForce='GTX', price=priceForCloseLongOrder)
                # -----------------------------------#

                time.sleep(time_to_cool_down)

        if (
                DOGEBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and DOGEBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and DOGEBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and DOGEBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and DOGEBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
        ):
            time.sleep(time_to_wait_one_more_check)

            if (
                    DOGEBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL", "SELL")
                    and DOGEBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL", "SELL")
                    and DOGEBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL", "SELL")
                    and DOGEBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL", "SELL")
                    and DOGEBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL", "SELL")
            ):
                # open short order and close short order#
                priceForOpenShortOrder = format(Decimal(client.futures_coin_ticker(symbol='DOGEUSD_PERP')[0]['lastPrice']), '.5f')
                client.futures_create_order(symbol='DOGEBUSD', side='SELL', positionSide='SHORT', type='LIMIT',
                                            quantity=60,
                                            timeInForce='GTX', price=priceForOpenShortOrder )
                time.sleep(1)

                priceForCloseShortOrder = format(
                    Decimal(client.futures_position_information(symbol='DOGEBUSD')[2]['entryPrice']), '.5f')
                amtForCloseShortOrder = format(
                    abs(Decimal(client.futures_position_information(symbol='DOGEBUSD')[2]['positionAmt'])))

                print("priceForCloseShortOrder", priceForCloseShortOrder)
                print("amtForCloseShortOrder", amtForCloseShortOrder)

                client.futures_create_order(symbol='DOGEBUSD', side='BUY', positionSide='SHORT', type='LIMIT',
                                            quantity=amtForCloseShortOrder,
                                            timeInForce='GTX', price=priceForCloseShortOrder)
                # -----------------------------------#

                time.sleep(time_to_cool_down)

    except Exception as e:
        print("Function errored out!", e)
        print("Retrying ... ")
