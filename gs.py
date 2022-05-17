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
            "t",
            "-sm",
            "t"

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
            "t",
            "-sm",
            "t"

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
            "t",
            "-sm",
            "t"

        ]
    )


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=eth_gs)
    p2 = multiprocessing.Process(target=ada_gs)
    p3 = multiprocessing.Process(target=doge_gs)
    p1.start()
    p2.start()
    p3.start()
