#!/bin/bash

krannumber=`echo $QUERY_STRING | sed s/[^0-9]//g`
kranstatus=`echo $QUERY_STRING | awk -F ":" '{print $2}'`
#echo "$krannumber $kranstatus" > /var/www/cgi-bin/control
#echo "$krannumber $kranstatus"
#krannumber=$1
#kranstatus=$2
echo "$krannumber $kranstatus"

[ $kranstatus = "open" ] && krangpiopin="22"
[ $kranstatus = "close" ] && krangpiopin="10"
[ $kranstatus = "half" ] && krangpiopin="22"

if [ ! -L /sys/class/gpio/gpio$krangpiopin ]; then
	echo $krangpiopin > /sys/class/gpio/export
sleep 1
	echo out > /sys/class/gpio/gpio$krangpiopin/direction
sleep 1
	echo 1 > /sys/class/gpio/gpio$krangpiopin/value
sleep 1
fi

echo 0 > /sys/class/gpio/gpio$krangpiopin/value
[ $kranstatus = "half" ] && sleep 3 || sleep 7
echo 1 > /sys/class/gpio/gpio$krangpiopin/value
echo /sys/class/gpio/gpio$krangpiopin/value
/usr/bin/curl -k "http://domoticz:8080/json.htm?type=command&param=switchlight&idx=42&switchcmd=Set%20Level&level=0"
