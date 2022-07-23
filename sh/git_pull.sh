#!/bin/bash

tmux kill-session
cd /root/apollo
git stash
git pull https://github.com/ka1myk/apollo.git
cp /root/apollo/passivbot/config.json /root/passivbot/configs/live/config.json
cp /root/apollo/passivbot/config.yaml /root/passivbot/manager/config.yaml
cd cd /root/apollo
chmod +x *.sh