from tradingview_ta import TA_Handler, Interval, Exchange
from variables import time_to_create_order, time_to_wait_one_more_check, time_to_cool_down, time_to_create_gs_order
import subprocess
import time

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
        gs_order = subprocess.Popen(
            [
                "python3",
                "passivbot.py",
                "binance_01",
                "ADABUSD",
                "/root/passivbot_configs/long.json",
                "-lm",
                "gs",
                "-sm",
                "gs"
            ]
        )
        time.sleep(time_to_create_gs_order)
        gs_order.terminate()

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
                    )

            ):
                hedge_order = subprocess.Popen(
                    [
                        "python3",
                        "passivbot.py",
                        "binance_01",
                        "ADABUSD",
                        "/root/passivbot_configs/long.json",
                        "-lm",
                        "n",
                        "-sm",
                        "n"
                    ]
                )
                time.sleep(time_to_create_order)
                hedge_order.terminate()
                time.sleep(time_to_cool_down)

    except Exception as e:
        print("Function errored out!", e)
        print("Retrying ... ")
