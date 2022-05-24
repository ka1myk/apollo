-DONE-
btc - 	math random and fix delay 											   -> open long OR short
eth - 	liquidation 														   -> open long OR short
gmt - 	check STRONG BUY or STRONG SELL 									   -> open long AND short
doge - 	check STRONG BUY or STRONG SELL, wait, check STRONG BUY or STRONG SELL -> open long OR short
ada - 	check STRONG BUY or STRONG SELL, wait, check STRONG BUY or STRONG SELL -> open long AND short
xrp - 	check STRONG BUY or STRONG SELL, wait, check STRONG BUY or STRONG SELL -> open REVERSE long OR REVERSE short
bnb - 	check STRONG BUY or STRONG SELL (NASDAQ-IXIC)						   -> open REVERSE long OR REVERSE short

-TODO-
near - 	math random and random delay										   -> open long OR short
avax -  arbitrage 
sol -   taker Buy/Sell Volume
1) change leverage dynamically 
2) trailing stop profit
3) change min_markup dynamically
4) open (MARKET) and close orders (GTX) in batch with get position and profit percent from variables.json

https://docs.glassnode.com/api/transactions#percent-volume-in-profit
https://coinglass.github.io/API-Reference/#exchange-open-interest
https://alternative.me/crypto/
https://www.coingecko.com/en/api
https://www.cryptometer.io/liquidation-data

-------
Guide to deploy:
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