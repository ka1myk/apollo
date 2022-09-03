- Testing for a week from ... to ...
- Goal: to identify the optimal ratio of the percentage of profit and timeframe
- Methodology:
- Choose 3 profits: 0.1%, 0.5%, 1%
- Choose 6 timeframes in minutes: 1440, 720, 360, 180, 90, 45, 22.5
- Thus we get 21 unique combinations
																
![изображение](https://user-images.githubusercontent.com/22070331/184793716-0212825f-f737-420e-a324-ed740a4f8ea7.png)


- for test will use hardcode "coin.py" for every coin, simultaneously open long and short, manager with websocket from passivbot and dedicated vps
- 784*3=2352 busd for all 21 unique combinations
add week_test.xlsx to edit result
-------
Useful links:
https://docs.glassnode.com/api/transactions#percent-volume-in-profit
https://coinglass.github.io/API-Reference/#exchange-open-interest
https://alternative.me/crypto/
https://www.coingecko.com/en/api
https://www.cryptometer.io/liquidation-data
https://sammchardy.github.io/binance-order-filters/
-------
Commands:

1)
apt-get update && 
apt-get upgrade && 
apt-get install git && 
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
--------
crontab -e
--------
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/local/bin/futuresboard
@reboot sleep 90; /bin/bash -c cd /root/futuresboard && futuresboard

