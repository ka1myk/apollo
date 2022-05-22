#!/bin/bash

python3 /root/binance_strategies/notify.py
sleep 0.5
tmuxp load /root/binance_strategies/session.yaml
