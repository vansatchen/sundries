#!/usr/bin/env python3

import os
import os.path
import subprocess
import time
import requests

domomq135 = 'http://domoticz:8080/json.htm?type=command&param=udevice&idx=35&nvalue=0&svalue='
domowcfan = 'http://domoticz:8080/json.htm?type=command&param=switchlight&idx=40&switchcmd=Set%20Level&level='
checktimes=12
controltxt='/opt/fancontrol/control.txt'

if os.path.isfile(controltxt):
    controlread=open(controltxt, 'r')
    forcerun=int(controlread.read().strip())
    controlread.close()
    if(forcerun >= 1):
        exit(10)
else:
    forcerun=0

if not os.path.islink('/sys/class/gpio/gpio9'):
    subprocess.call(["/bin/echo 9 > /sys/class/gpio/export"], shell=True)
    time.sleep(1)
    subprocess.call(["/bin/echo out > /sys/class/gpio/gpio9/direction"], shell=True)

datchikstart=subprocess.getoutput(["/opt/fancontrol/mq135.py"])
datchikstart=int(datchikstart)

time.sleep(1)
for x in range(1, checktimes):
    datchikstat=subprocess.getoutput(["/opt/fancontrol/mq135.py"])
    datchikstat=int(datchikstat)
    # Update mq135 stat
    requests.get(domomq135 + str(datchikstat))
    # Update Fan status
    lvlup = datchikstart + 5
    lvldn = datchikstart - 2
    if(datchikstat >= lvlup):
        subprocess.call(["/bin/echo 1 > /sys/class/gpio/gpio9/value"], shell=True)
        requests.get(domowcfan + str('70'))
    if(datchikstat <= lvldn):
        time.sleep(1)
        subprocess.call(["/bin/echo 0 > /sys/class/gpio/gpio9/value"], shell=True)
        if(x == 9):
            requests.get(domowcfan + str('0'))
    time.sleep(9)
