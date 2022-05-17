#!/bin/bash

sh /root/passivbot_configs/git_pull.sh
tmux kill-session
tmuxp load /root/passivbot_configs/session.yaml
