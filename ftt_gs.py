import subprocess

gs_order = subprocess.Popen(
    [
        "python3",
        "passivbot.py",
        "binance_01",
        "FTTBUSD",
        "/root/passivbot_configs/long.json",
        "-gs"
    ]
)
