import multiprocessing
import subprocess


def eth_gs():
    subprocess.Popen(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "ETHBUSD",
            "/root/binance_strategies/long.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )


def ada_gs():
    subprocess.Popen(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "ADABUSD",
            "/root/binance_strategies/long.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )


def doge_gs():
    subprocess.Popen(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "DOGEBUSD",
            "/root/binance_strategies/long.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )


def gmt_gs():
    subprocess.Popen(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "GMTBUSD",
            "/root/binance_strategies/long.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )


def btc_gs():
    subprocess.Popen(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "BTCBUSD",
            "/root/binance_strategies/long.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )


def xrp_gs():
    subprocess.Popen(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "XRPBUSD",
            "/root/binance_strategies/long.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )


def bnb_gs():
    subprocess.Popen(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "BNBBUSD",
            "/root/binance_strategies/long.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=eth_gs)
    p2 = multiprocessing.Process(target=ada_gs)
    p3 = multiprocessing.Process(target=doge_gs)
    p4 = multiprocessing.Process(target=gmt_gs)
    p5 = multiprocessing.Process(target=btc_gs)
    p6 = multiprocessing.Process(target=xrp_gs)
    p7 = multiprocessing.Process(target=bnb_gs)
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
