#!/bin/bash

ctrlfile=/opt/fancontrol/control.txt
wcfcpid=/run/wcfancontrol/wcfancontrol.pid

[ -f $wcfcpid ] && kill -9 $(cat $wcfcpid)
killall fancontrol.sh
killall sleep
killall fancontrol.py
echo $$ > $wcfcpid

fanruntime=`echo $QUERY_STRING | sed s/[^0-9]//g`
#fanruntime=$1
echo $fanruntime > $ctrlfile
fanrunstatus=`echo $QUERY_STRING | awk -F ":" '{print $2}'`
#fanrunstatus=$2
if [ ! -L /sys/class/gpio/gpio9 ]; then
	echo 9 > /sys/class/gpio/export
	sleep 1
	echo out > /sys/class/gpio/gpio9/direction
fi
if [ $fanrunstatus = "On" ]; then
	echo 1 > /sys/class/gpio/gpio9/value
	[ $fanruntime == 15 ] && domzstat=10
	[ $fanruntime == 30 ] && domzstat=30
	[ $fanruntime == 60 ] && domzstat=50
	/usr/bin/curl -k "http://domoticz:8080/json.htm?type=command&param=switchlight&idx=40&switchcmd=Set%20Level&level=$domzstat"
	sleep "$fanruntime"m
	echo 0 > /sys/class/gpio/gpio9/value
fi
if [ $fanrunstatus = "Off" ]; then
	echo 0 > /sys/class/gpio/gpio9/value
	[ $fanruntime == 15 ] && domzstat=20
	[ $fanruntime == 30 ] && domzstat=40
	[ $fanruntime == 60 ] && domzstat=60
	/usr/bin/curl -k "http://domoticz:8080/json.htm?type=command&param=switchlight&idx=40&switchcmd=Set%20Level&level=$domzstat"
	sleep "$fanruntime"m
fi
echo 0 > $ctrlfile
rm -f $wcfcpid

exit 0
