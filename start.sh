#!/bin/bash

python3 /root/passivbot_configs/notify.py
sleep 0.5
tmuxp load /root/passivbot_configs/session.yaml
