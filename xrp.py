from tradingview_ta import TA_Handler, Interval, Exchange
import time
import subprocess

XRPBUSDPERP_1 = TA_Handler(
    symbol="XRPBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)

XRPBUSDPERP_5 = TA_Handler(
    symbol="XRPBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES
)

while True:
    if XRPBUSDPERP_1.get_analysis().summary['RECOMMENDATION'] in ("STRONG_BUY", "BUY") and XRPBUSDPERP_5.get_analysis().summary['RECOMMENDATION'] in ("STRONG_BUY", "BUY"):
        l = subprocess.Popen(['python3', 'passivbot.py', 'binance_kalmykov', 'XRPBUSD', 'passivbot_configs/long.json'])
        time.sleep(45)
        l.terminate()
    else:
        w = subprocess.Popen(['python3', 'passivbot.py', 'binance_kalmykov', 'XRPBUSD', 'passivbot_configs/long.json', '-lm', 'gs'])
        time.sleep(45)
        w.terminate()