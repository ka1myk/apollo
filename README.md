- Testing for a week from ... to ...
- Goal: to identify the optimal ratio of the percentage of Profit and timeframe
- Methodology:
- Choose 3 profits: 0.1%, 0.5%, 1%
- We choose 6 timeframes in minutes: 1440, 720, 360, 90, 45, 22.5
- Thus we get 18 unique combinations
	
![изображение](https://user-images.githubusercontent.com/22070331/184557456-ca02f68d-dac9-48e1-ac99-9776a24be289.png)

- for test wiil use hardcode "coin.py", manager from passivbot and dedicated vps

-------
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
1)
apt-get update && 
apt-get upgrade && 
apt-get install git && 
apt-get install tmux && 
apt-get install tmuxp && 
apt-get install systemd-timesyncd && 
apt-get install python3-pip

2)
cd &&
git clone https://github.com/ka1myk/apollo.git &&
cd apollo && 
pip3 install -r requirements.txt

3)
cd && 
git clone https://github.com/ecoppen/futuresboard.git && 
cd futuresboard && 
python3 -m pip install . &&
mv config/config.json.example config/config.json

4)
cd && 
git clone https://github.com/enarjord/passivbot.git && 
cd passivbot &&
pip3 install -r requirements_liveonly.txt &&
cp /root/apollo/passivbot/api-keys.json /root/passivbot/api-keys.json &&
cp /root/apollo/passivbot/config.json /root/passivbot/configs/live/config.json &&
cp /root/apollo/passivbot/config.yaml /root/passivbot/manager/config.yaml &&
cd &&
cd /root/passivbot/manager &&
nano constants.py 
--------
crontab -e
--------
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/local/bin/futuresboard
@reboot sleep 90; /bin/bash -c /root/apollo/sh/start.sh
