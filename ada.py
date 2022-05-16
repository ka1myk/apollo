import json
from decimal import Decimal

from tradingview_ta import TA_Handler, Interval, Exchange
from variables import time_to_create_order, time_to_wait_one_more_check, time_to_cool_down, time_to_create_gs_order
import time
from binance.client import Client

with open('/root/passivbot/api-keys.json') as p:
    creds = json.load(p)

client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

ADABUSDPERP_INTERVAL_1_MINUTE = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)

ADABUSDPERP_INTERVAL_5_MINUTES = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES
)

ADABUSDPERP_INTERVAL_15_MINUTES = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_15_MINUTES
)

ADABUSDPERP_INTERVAL_30_MINUTES = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_30_MINUTES
)

ADABUSDPERP_INTERVAL_1_HOUR = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_HOUR
)

ADABUSDPERP_INTERVAL_2_HOURS = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_2_HOURS
)

ADABUSDPERP_INTERVAL_4_HOURS = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_4_HOURS
)

ADABUSDPERP_INTERVAL_1_DAY = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_DAY
)

while True:
    try:

        if (
                (
                        ADABUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_BUY", "BUY")
                        and ADABUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_BUY", "BUY")
                        and ADABUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_BUY", "BUY")
                        and ADABUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_BUY", "BUY")
                        and ADABUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_BUY", "BUY")
                )

                or

                (
                        ADABUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_SELL", "SELL")
                        and ADABUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_SELL", "SELL")
                        and ADABUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_SELL", "SELL")
                        and ADABUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_SELL", "SELL")
                        and ADABUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_SELL", "SELL")
                )

        ):
            time.sleep(time_to_wait_one_more_check)

            if (

                    (
                            ADABUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_BUY", "BUY")
                            and ADABUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_BUY", "BUY")
                            and ADABUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_BUY", "BUY")
                            and ADABUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_BUY", "BUY")
                            and ADABUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_BUY", "BUY")
                    )

                    or

                    (
                            ADABUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_SELL", "SELL")
                            and ADABUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_SELL", "SELL")
                            and ADABUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_SELL", "SELL")
                            and ADABUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_SELL", "SELL")
                            and ADABUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_SELL", "SELL")
                    )

            ):
                # open long order and close long order#
                priceForOpenLongOrder = format(Decimal(client.futures_coin_ticker(symbol='ADAUSD_PERP')[0]['lastPrice']), '.4f')
                
                client.futures_create_order(symbol='ADABUSD', side='BUY', positionSide='LONG', type='LIMIT',
                                            quantity=10,
                                            timeInForce='GTX', price=priceForOpenLongOrder)
                time.sleep(1)

                priceForCloseLongOrder = format(
                    Decimal(client.futures_position_information(symbol='ADABUSD')[1]['entryPrice']), '.4f')
                amtForCloseLongOrder = Decimal(client.futures_position_information(symbol='ADABUSD')[1]['positionAmt'])

                print("priceForCloseLongOrder", priceForCloseLongOrder)
                print("amtForCloseLongOrder", amtForCloseLongOrder)

                client.futures_create_order(symbol='ADABUSD', side='SELL', positionSide='LONG', type='LIMIT',
                                            quantity=amtForCloseLongOrder,
                                            timeInForce='GTX', price=priceForCloseLongOrder)
                # -----------------------------------#

                # open short order and close short order#
                priceForOpenShortOrder = format(Decimal(client.futures_coin_ticker(symbol='ADAUSD_PERP')[0]['lastPrice']), '.4f')
                client.futures_create_order(symbol='ADABUSD', side='SELL', positionSide='SHORT', type='LIMIT',
                                            quantity=10,
                                            timeInForce='GTX', price=priceForOpenShortOrder)
                time.sleep(1)

                priceForCloseShortOrder = format(
                    Decimal(client.futures_position_information(symbol='ADABUSD')[2]['entryPrice']), '.4f')
                amtForCloseShortOrder = format(
                    abs(Decimal(client.futures_position_information(symbol='ADABUSD')[2]['positionAmt'])))

                print("priceForCloseShortOrder", priceForCloseShortOrder)
                print("amtForCloseShortOrder", amtForCloseShortOrder)

                client.futures_create_order(symbol='ADABUSD', side='BUY', positionSide='SHORT', type='LIMIT',
                                            quantity=amtForCloseShortOrder,
                                            timeInForce='GTX', price=priceForCloseShortOrder)
                # -----------------------------------#

                time.sleep(time_to_cool_down * 20)

    except Exception as e:
        print("Function errored out!", e)
        print("Retrying ... ")
