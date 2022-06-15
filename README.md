BTC, ETH, SOL, XRP, ADA, BNB        - coinglass liquidation
DOGE, FTT, AVAX, NEAR, APE, GMT     - tradingview signals
FTM, GAl                            - random
-------
DOGE - 	check BUY or SELL, wait, check BUY or SELL      -> open long OR short
FTT  -  check STRONG BUY or STRONG SELL                 -> open long OR short
AVAX - 	check BUY or SELL, wait, check BUY or SELL      -> open REVERSE long OR REVERSE short
NEAR - 	check STRONG BUY or STRONG SELL             	-> open REVERSE long OR REVERSE short
APE  - 	check BUY or SELL, wait, check BUY or SELL      -> open long AND short
GMT  - 	check STRONG BUY or STRONG SELL 			    -> open long AND short
-------
DODO, ANC, GALA, TRX, 1000LUNC, LUNA2 - TBD
-------
carousel of strategies and symbols
arbitrage
taker Buy/Sell Volume
change leverage dynamically
trailing stop profit
change min_markup dynamically
open (MARKET) and close orders (GTX) in batch with get position and profit percent from variables.json
-------
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
cd &&
git clone https://github.com/ka1myk/binance_strategies.git &&
cd binance_strategies && 
pip3 install -r requirements.txt &&
git pull https://github.com/ka1myk/binance_strategies.git
--------
crontab -e
--------
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/local/bin/futuresboard
@reboot sleep 90; /bin/bash -c /root/binance_strategies/start.sh
0 */12 * * * /bin/bash -c /root/binance_strategies/restart.sh