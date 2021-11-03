#!/usr/bin/python3

import sys

txtbd = "/var/lib/asterisk/documentation/text.txt"

if len(sys.argv) < 2:
    calleridName = "anonymous"
else:
    calleridNum = sys.argv[1]
    if not calleridNum.isdigit():
        calleridName = "anonymous"

if len(calleridNum) == 4:
    calleridNum = calleridNum[1:4]

with open(txtbd, 'r') as file:
    for line in file:
        if calleridNum in line:
            calleridName = line.split(';')[0]

print("SET VARIABLE calleridvar \"" + calleridName + "\"")
