from tradingview_ta import TA_Handler, Interval, Exchange
import time
import subprocess

ADABUSDPERP_1 = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)

ADABUSDPERP_5 = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES
)

ADABUSDPERP_15 = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_15_MINUTES
)

while True:
    if ADABUSDPERP_1.get_analysis().summary['RECOMMENDATION'] in ("STRONG_BUY", "BUY") and ADABUSDPERP_5.get_analysis().summary['RECOMMENDATION'] in ("STRONG_BUY", "BUY") and ADABUSDPERP_15.get_analysis().summary['RECOMMENDATION'] in ("STRONG_BUY", "BUY"):
        l = subprocess.Popen(['python3', 'passivbot.py', 'binance', 'ADABUSD', 'passivbot_configs/long.json'])
        time.sleep(45)
        l.terminate()
    else:
        w = subprocess.Popen(['python3', 'passivbot.py', 'binance', 'ADABUSD', 'passivbot_configs/long.json', '-lm', 'gs'])
        time.sleep(45)
        w.terminate()
