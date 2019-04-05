#!/bin/bash

url=http://192.168.0.40:5046

current=$PWD

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


command -v curl >/dev/null 2>&1 || { echo -e "${RED}curl is required but it's not installed.  Aborting."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo -e "${RED}python3 is required but it's not installed.  Aborting."; exit 1; }

echo -e "${GREEN}Requirements OK. Starting downloads...${NC}"

function npath()
{
    dest=$current/$1
    mkdir -p $dest
    echo "$1"
}

cd $current
fld=$(npath) && cd $current/$fld
# curl -O $url/get/config.json
curl -O $url/get/distributor.py
curl -O $url/get/requirements.txt
curl -O $url/get/run.py
curl -O $url/get/market_maker.py
curl -O $url/get/README.md

# fld=$(npath server/continuous_exchange) && cd $current/$fld
# curl -O $url/get/$fld/exchangeconfig.textproto

# fld=$(npath mine/logs) && cd $current/$fld

fld=$(npath mine) && cd $current/$fld
# curl -O $url/get/$fld/run.py
curl -O $url/get/$fld/utils.py
curl -O $url/get/$fld/ws_http_server.py

# fld=$(npath mine/scripts) && cd $current/$fld
# curl -O $url/get/$fld/launch
# curl -O $url/get/$fld/running
# chmod +x launch
# chmod +x running

fld=$(npath mine/trader) && cd $current/$fld
curl -O $url/get/$fld/client_base.py
curl -O $url/get/$fld/client_send.py
curl -O $url/get/$fld/Instrument.py
curl -O $url/get/$fld/Markets.py
curl -O $url/get/$fld/Option.py
curl -O $url/get/$fld/Orders.py
curl -O $url/get/$fld/Trader.py
curl -O $url/get/$fld/Logs.py

fld=$(npath mine/trader/server) && cd $current/$fld
curl -O $url/get/$fld/favicon.ico
curl -O $url/get/$fld/index.html

fld=$(npath mine/trader/server/libs) && cd $current/$fld
curl -O $url/get/$fld/d3.v5.min.js
curl -O $url/get/$fld/jquery.js
curl -O $url/get/$fld/pure.css

fld=$(npath mine/trader/server/src) && cd $current/$fld
curl -O $url/get/$fld/cases.js
curl -O $url/get/$fld/chart.js
curl -O $url/get/$fld/charts.js
curl -O $url/get/$fld/common.css
curl -O $url/get/$fld/grid.js
curl -O $url/get/$fld/start.js
curl -O $url/get/$fld/updater.js
curl -O $url/get/$fld/ws.js

# ==================================================================
# ==================================================================
# =============== downloads done, now env + finish =================
# ==================================================================
# ==================================================================

cd $current
file="requirements.txt"
if [ -f "$file" ]
then
	echo -e "${GREEN}ALL GOOD for now..."
  echo "Setting environment...."
else
	echo -e "${RED}$file not found. Should be there. Exiting..."
  exit 1
fi
