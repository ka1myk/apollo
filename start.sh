#!/bin/bash

python3 notify.py
sleep 0.5
tmuxp load /passivbot/passivbot_configs/session.yaml
