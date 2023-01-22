import secrets
import subprocess

go = ["spot.py", "margin.py", "futures.py", "earn.py"]

subprocess.call(secrets.choice(go), shell=True)