#!/usr/bin/env python
# Program for gas sensor MQ135 + ADC-DAC PCF8591P
# 2016 http://ph0en1x.net

import os
import time
from smbus import SMBus

DEV_ADDR = 0x48
adc_channel = 0b1000010 # 0x42 (input AIN2 for ADC + use DAC)
dac_channel = 0b1000000 # 0x40

bus = SMBus(1)          # 1 - I2C bus address for RPi rev.2

while(1):
#    os.system('clear')
#    print("Press Ctrl C to stop...\n")
    # read sensor value from ADC
    bus.write_byte(DEV_ADDR, adc_channel)
    bus.read_byte(DEV_ADDR)
    bus.read_byte(DEV_ADDR)
    value = bus.read_byte(DEV_ADDR)
#    print 'AIN value = ' + str(value)
    print str(value)
    # compare value from ADC and set value in DAC
    if value > 120:
        bus.write_byte_data(DEV_ADDR, dac_channel, 220)
    else:
        bus.write_byte_data(DEV_ADDR, dac_channel, 0)
    # pause 100 milliseconds
    time.sleep(0.1)
    raise SystemExit
