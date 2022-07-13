#!/bin/bash

tmux kill-session
cd /root/binance_strategies
git stash
git pull https://github.com/ka1myk/binance_strategies.git onlyRandom
chmod +x *.sh