from tradingview_ta import TA_Handler, Interval, Exchange
import time
import subprocess

BTCBUSDPERP_1 = TA_Handler(
    symbol="BTCBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)

BTCBUSDPERP_5 = TA_Handler(
    symbol="BTCBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES
)

while True:
    if BTCBUSDPERP_1.get_analysis().summary['RECOMMENDATION'] in ("STRONG_BUY", "BUY") and BTCBUSDPERP_5.get_analysis().summary['RECOMMENDATION'] in ("STRONG_BUY", "BUY"):
        l = subprocess.Popen(['python3', 'passivbot.py', 'binance_kalmykov', 'BTCBUSD', 'passivbot_configs/long.json'])
        time.sleep(45)
        l.terminate()
    else:
        w = subprocess.Popen(['python3', 'passivbot.py', 'binance_kalmykov', 'BTCBUSD', 'passivbot_configs/long.json', '-lm', 'gs'])
        time.sleep(45)
        w.terminate()