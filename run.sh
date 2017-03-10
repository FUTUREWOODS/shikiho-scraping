#!/bin/sh
NUM=2050
while true ; do
echo $NUM
python scrape.py getinfo https://shikiho.jp/tk/stock/info/$NUM
NUM=`expr $NUM + 1`
sleep 5
done
