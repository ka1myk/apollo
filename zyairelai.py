import multiprocessing
import subprocess


def futures-hero():
    subprocess.Popen(
        [
            "python3.8",
            "/root/futures-hero/run.py"
        ]
    )


def long-term-low-leverage():
    subprocess.Popen(
        [
            "python3.8",
            "/root/long-term-low-leverage/trade_binance.py"
        ]
    )


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=futures-hero)
    p2 = multiprocessing.Process(target=long-term-low-leverage)
    p1.start()
    p2.start()
