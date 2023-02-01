# TODO add binance another user as argument
import secrets
import subprocess

go = ["cd && python3 /root/apollo/spot.py",
      "cd && python3 /root/apollo/margin.py",
      "cd && python3 /root/apollo/futures.py"]

subprocess.call(secrets.choice(go), shell=True)