#Useful links:
#https://docs.glassnode.com/api/transactions#percent-volume-in-profit
#https://coinglass.github.io/API-Reference/#exchange-open-interest
#https://alternative.me/crypto/
#https://www.coingecko.com/en/api
#https://www.cryptometer.io/liquidation-data
#https://www.futuresboard.xyz/

apt-get update &&
apt-get upgrade &&
apt-get install git &&
apt-get install systemd-timesyncd &&
apt-get install python3-pip &&
apt-get install tmuxp &&
apt-get install fail2ban &&
cd && git clone https://github.com/ka1myk/apollo.git && cd apollo && pip3 install -r requirements.txt
cd && git clone https://github.com/ecoppen/futuresboard.git && cd futuresboard && python3 -m pip install . && mv config/config.json.example config/config.json &&
cd && crontab -e