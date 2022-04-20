import subprocess

gs_order = subprocess.Popen(
    [
        "python3",
        "passivbot.py",
        "binance_01",
        "BTCBUSD",
        "/root/passivbot_configs/long.json",
        "-gs"
    ]
)
