import multiprocessing
import subprocess


def gs():
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
    p1 = multiprocessing.Process(target=gs)
    p1.start()
