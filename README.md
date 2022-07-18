Useful links:
https://docs.glassnode.com/api/transactions#percent-volume-in-profit
https://coinglass.github.io/API-Reference/#exchange-open-interest
https://alternative.me/crypto/
https://www.coingecko.com/en/api
https://www.cryptometer.io/liquidation-data
https://sammchardy.github.io/binance-order-filters/
-------
Guide to deploy:
https://www.futuresboard.xyz/guides.html
-------
Commands:
apt-get update && 
apt-get upgrade && 
apt-get install git && 
apt-get install tmux && 
apt-get install tmuxp && 
apt-get install systemd-timesyncd && 
apt-get install python3-pip &&

cd &&
git clone https://github.com/ka1myk/apollo.git &&
cd apollo && 
pip3 install -r requirements.txt

cd && 
git clone https://github.com/ecoppen/futuresboard.git && 
cd futuresboard && 
python3 -m pip install . &&
mv config/config.json.example config/config.json &&

cd && 
git clone https://github.com/enarjord/passivbot.git && 
cd passivbot &&
pip3 install -r requirements_liveonly.txt &&
cp /root/apollo/passivbot/api-keys.json /root/passivbot/api-keys.json &&
cp /root/apollo/passivbot/config.json /root/passivbot/configs/live/config.json &&
cp /root/apollo/passivbot/config.yaml /root/passivbot/manager/config.yaml
--------
crontab -e
--------
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/local/bin/futuresboard
@reboot sleep 90; /bin/bash -c /root/apollo/sh/start.sh
0 0 * * * /bin/bash -c /root/apollo/sh/restart.sh