Guide:
https://www.futuresboard.xyz/guides.html
--------
Commands:
apt-get update && 
apt-get upgrade && 
cd && 
git clone https://github.com/ecoppen/futuresboard.git && 
cd futuresboard && 
python3 -m pip install . && 
mv config/config.json.example config/config.json && 
apt-get install git && 
apt-get install tmux && 
apt-get install tmuxp && 
apt-get install systemd-timesyncd && 
apt-get install python3-pip && 
cd && 
git clone https://github.com/enarjord/passivbot.git && 
cd passivbot && pip3 install -r requirements_liveonly.txt && 
pip3 install -r requirements_liveonly.txt &&
mv api-keys.example.json api-keys.json &&
git clone https://github.com/ka1myk/binance_strategies.git &&
cd binance_strategies && pip3 install -r requirements.txt &&
git pull https://github.com/ka1myk/binance_strategies.git
--------
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/local/bin/futuresboard
@reboot sleep 10; /bin/bash -c /root/binance_strategies/start.sh
#*/5 * * * * sh /root/binance_strategies/git_pull.sh && cd && cd binance_strategies && chmod +x start.sh git_pull.sh