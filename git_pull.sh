#!/bin/bash

cd /root/binance_strategies
git stash
git pull https://github.com/ka1myk/binance_strategies.git dev
chmod +x *.sh