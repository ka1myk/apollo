#!/bin/bash

tmux kill-session
cd /root/apollo
git stash
git pull https://github.com/ka1myk/apollo.git
cp /root/apollo/passivbot/config.json /root/passivbot/configs/live/config.json
cp /root/apollo/passivbot/config0_1.json /root/passivbot/configs/live/config0_1.json
cp /root/apollo/passivbot/config0_5.json /root/passivbot/configs/live/config0_5.json
cp /root/apollo/passivbot/config1.json /root/passivbot/configs/live/config1.json
cp /root/apollo/passivbot/config.yaml /root/passivbot/manager/config.yaml
cd
cd /root/apollo/sh
chmod +x *.sh
