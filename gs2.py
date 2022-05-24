import multiprocessing
import subprocess


def gs2():
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


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=gs2)
    p1.start()
