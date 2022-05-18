import multiprocessing
import subprocess


def futures_hero():
    subprocess.Popen(
        [
            "python3.8",
            "/root/futures-hero/run.py"
        ]
    )


def long_term_low_leverage():
    subprocess.Popen(
        [
            "python3.8",
            "/root/long-term-low-leverage/trade_binance.py"
        ]
    )


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=futures_hero)
    p2 = multiprocessing.Process(target=long_term_low_leverage)
    p1.start()
    p2.start()
