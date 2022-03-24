# passivbot_configs

Guide:
https://www.futuresboard.xyz/guides.html

Commands:
apt-get update && apt-get upgrade && cd && git clone https://github.com/ecoppen/futuresboard.git && cd futuresboard && python3 -m pip install . && mv config/config.json.example config/config.json && apt-get install git && apt-get install tmux && apt-get install tmuxp && apt-get install systemd-timesyncd && apt-get install python3-pip && cd && git clone https://github.com/enarjord/passivbot.git && cd passivbot && pip3 install -r requirements_liveonly.txt && pip3 install -r requirements_liveonly.txt && mv api-keys.example.json api-keys.json && git clone https://github.com/ka1myk/passivbot_configs.git && cd passivbot_configs && pip3 install -r requirements.txt && git pull https://github.com/ka1myk/passivbot_configs.git
--------
@reboot sleep 10; /bin/bash -c /root/passivbot_configs/start.sh
*/5 * * * * sh /root/passivbot_configs/git_pull.sh && cd && cd passivbot_configs && chmod +x start.sh git_pull.sh
