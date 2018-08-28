#!/bin/bash

checktimes="12"

controltxt="/opt/fancontrol/control.txt"
if [ -f $controltxt ]; then
	forcerun=`cat $controltxt`
	[ $forcerun -ge 1 ] && exit 10
else
	forcerun=0
fi
if [ ! -L /sys/class/gpio/gpio9 ]; then
	echo 9 > /sys/class/gpio/export
	sleep 1
	echo out > /sys/class/gpio/gpio9/direction
fi
datchikstart=`/usr/bin/python /opt/fancontrol/mq135.py`
sleep 1
for ((i = 1; i < $checktimes; i++))
do
	datchikstat=`/usr/bin/python /opt/fancontrol/mq135.py`
	# Update mq135 stat
	[ $datchikstat = "0" ] || /usr/bin/curl -k "http://domoticz:8080/json.htm?type=command&param=udevice&idx=35&nvalue=0&svalue=$datchikstat"
	echo $datchikstat
	# Update Fan status
	let "lvlup = $datchikstart + 5"
	let "lvldn = $datchikstart - 2"
	if [ $datchikstat -ge $lvlup ]; then
		echo 1 > /sys/class/gpio/gpio9/value
		/usr/bin/curl -k "http://domoticz:8080/json.htm?type=command&param=switchlight&idx=40&switchcmd=Set%20Level&level=70"
	fi
	if [ $datchikstat -le $lvldn ]; then
		sleep 1
		echo 0 > /sys/class/gpio/gpio9/value
		[ $i == 3 ] && /usr/bin/curl -k "http://domoticz:8080/json.htm?type=command&param=switchlight&idx=40&switchcmd=Set%20Level&level=0"
	fi
	sleep 9
done
