#!/bin/bash

DHTDATA=`/usr/bin/python /home/user/DHT11_Python/dht11_example.py`
DHTDATA1=`echo $DHTDATA | awk '{print $1}'`
DHTDATA2=`echo $DHTDATA | awk '{print $2}'`
#echo Temp=$DHTDATA1
#echo Hum=$DHTDATA2
/usr/bin/curl -k "http://domoticz:8080/json.htm?type=command&param=udevice&idx=4&nvalue=0&svalue=$DHTDATA1;$DHTDATA2;1"

#/usr/local/bin/oled -t "" -t "$(date +%r)" -t "" -t "Temp = $DHTDATA1 'C" -t "" -t "Humidity = $DHTDATA2 %"
cd /home/user/ssd1306_rpi
./ssd1306oled r
./ssd1306oled +d "$(date +%R)"
./ssd1306oled +b "Temp = $DHTDATA1'C"
./ssd1306oled +c "Humidity = $DHTDATA2%"
./ssd1306oled s
sleep 25
cpuTemp0=$(cat /sys/class/thermal/thermal_zone0/temp)
cpuTemp1=$(($cpuTemp0/1000))
cpuTemp2=$(($cpuTemp0/100))
cpuTempM=$(($cpuTemp2 % $cpuTemp1))

#/usr/local/bin/oled -t ""  -t "$(date +%r)" -t "" -t "CPU temp=$cpuTemp1.$cpuTempM 'C" -t "" -t "GPU $(/opt/vc/bin/vcgencmd measure_temp)"
./ssd1306oled r
./ssd1306oled +d "$(date +%R)"
./ssd1306oled +b "CPU temp=$cpuTemp1.$cpuTempM'C"
./ssd1306oled +c "GPU $(/opt/vc/bin/vcgencmd measure_temp)"
./ssd1306oled s

exit 0
