import multiprocessing
import subprocess


def eth_gs():
    subprocess.Popen(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "ETHBUSD",
            "/root/passivbot_configs/long.json",
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
            "/root/passivbot_configs/long.json",
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
            "/root/passivbot_configs/long.json",
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
            "/root/passivbot_configs/long.json",
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
            "/root/passivbot_configs/long.json",
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
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
