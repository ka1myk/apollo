- Testing for a week from ... to ...
- Goal: to identify the optimal ratio of the percentage of profit and timeframe
- Methodology:
- Choose 3 profits: 0.1%, 0.5%, 1%
- Choose 6 timeframes in minutes: 1440, 720, 360, 180, 90, 45, 22.5
- Thus we get 21 unique combinations
																
https://docs.google.com/spreadsheets/d/15EQMQ0Xv4vw6TggzO8dzZKeQKcQMyw9bIjHTUHP9SQY/edit?usp=sharing


- for test will use hardcode "coin.py" for every coin, simultaneously open long and short, manager with websocket from passivbot and dedicated vps
- 784*3=2352 busd for all 21 unique combinations
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
shell=/bin/bash path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/local/bin/futuresboard
### futures ###
# 1W
8 2 * * MON cd /root/apollo/testing && python3 AUCTION.py
28 10 * * WED cd /root/apollo/testing && python3 GALA.py
48 18 * * SUN cd /root/apollo/testing && python3 FTM.py

# 3D
7 4 * * MON,THU cd /root/apollo/testing && python3 LDO.py
27 12 * * THU,FRI cd /root/apollo/testing && python3 DOGE.py
47 20 * * WED,SAT cd /root/apollo/testing && python3 ADA.py

# 1D
17 0 * * * cd /root/apollo/testing && python3 GMT.py
27 8 * * * cd /root/apollo/testing && python3 LEVER.py
47 16 * * * cd /root/apollo/testing && python3 ETH.py

# 12H
15 */12 * * * cd /root/apollo/testing && python3 LTC.py
35 */12 * * * cd /root/apollo/testing && python3 1000SHIB.py
55 */12 * * * cd /root/apollo/testing && python3 ANC.py

# 6H
10 */6 * * * cd /root/apollo/testing && python3 MATIC.py
40 */6 * * * cd /root/apollo/testing && python3 TLM.py
59 */6 * * * cd /root/apollo/testing && python3 DODO.py

# 3H
5  */3 * * * cd /root/apollo/testing && python3 NEAR.py
25 */3 * * * cd /root/apollo/testing && python3 APE.py
45 */3 * * * cd /root/apollo/testing && python3 LINK.py

# 1H
0  * * * * cd /root/apollo/testing && python3 SAND.py
20 * * * * cd /root/apollo/testing && python3 TRX.py
40 * * * * cd /root/apollo/testing && python3 XRP.py


