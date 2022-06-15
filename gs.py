import multiprocessing
import subprocess


async def coinglass_gs():
    subprocess.call(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "ADABUSD",
            "/root/binance_strategies/config.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )

    subprocess.call(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "BNBBUSD",
            "/root/binance_strategies/config.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )

    subprocess.call(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "BTCBUSD",
            "/root/binance_strategies/config.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )

    subprocess.call(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "ETHBUSD",
            "/root/binance_strategies/config.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )

    subprocess.call(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "SOLBUSD",
            "/root/binance_strategies/config.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )

    subprocess.call(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "XRPBUSD",
            "/root/binance_strategies/config.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )


async def random_gs():
    subprocess.call(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "FTMBUSD",
            "/root/binance_strategies/config.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )

    subprocess.call(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "GALBUSD",
            "/root/binance_strategies/config.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )


async def tradingview_gs():
    subprocess.call(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "APEBUSD",
            "/root/binance_strategies/config.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )

    subprocess.call(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "AVAXBUSD",
            "/root/binance_strategies/config.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )

    subprocess.call(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "DOGEBUSD",
            "/root/binance_strategies/config.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )

    subprocess.call(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "FTTBUSD",
            "/root/binance_strategies/config.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )

    subprocess.call(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "GMTBUSD",
            "/root/binance_strategies/config.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )

    subprocess.call(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "NEARBUSD",
            "/root/binance_strategies/config.json",
            "-lm",
            "gs",
            "-sm",
            "gs"

        ]
    )


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=coinglass_gs)
    p2 = multiprocessing.Process(target=tradingview_gs)
    p3 = multiprocessing.Process(target=random_gs)
    p1.start()
    p2.start()
    p3.start()