#!/usr/bin/python3

# Simle script makes report in xlsx file for remote job
# Developed by vansatchen

import sys
import shutil
import os
import datetime
from datetime import timedelta

# Check date arg exists and valid
def errorInfo():
    print("Usage: makeReport.py currentDate (example:20210525)")
    sys.exit(1)

if len(sys.argv) < 2:
    errorInfo()
else:
    baseDate = sys.argv[1]
    if not baseDate.isdigit() or not len(baseDate) == 8:
        errorInfo()

# Check date valid
baseYear = int(baseDate[0:4])
if baseYear < 2021 or baseYear > 2029:
    print("Invalid YEAR")
    sys.exit(1)

baseMonth = int(baseDate[4:6])
if baseMonth > 12:
    print("Invalid MONTH")
    sys.exit(1)

baseDay = int(baseDate[6:8])
if baseDay > 31:
    print("Invalid DAY")
    sys.exit(1)

# Calculate first day of week
baseDayVar = datetime.date(baseYear, baseMonth, baseDay)
baseWeekDay = baseDayVar.weekday()
firstDayOfWeek = datetime.datetime(baseYear, baseMonth, baseDay) - datetime.timedelta(days = baseWeekDay)

# Copy scel to temp dir
if not os.path.isdir("scel"):
    print("Directory scel not exists. Exiting...")
    sys.exit(1)

if not os.path.isdir("tmp"):
    shutil.copytree('scel', 'tmp')
else:
    print("Directory tmp exists. Exiting...")
    sys.exit(1)

# Make needed vars
deltaDay1 = (firstDayOfWeek - datetime.timedelta(days = 7)).strftime("%d.%m.%Y")
deltaDay2 = (firstDayOfWeek - datetime.timedelta(days = 6)).strftime("%d.%m.%Y")
deltaDay3 = (firstDayOfWeek - datetime.timedelta(days = 5)).strftime("%d.%m.%Y")
deltaDay4 = (firstDayOfWeek - datetime.timedelta(days = 4)).strftime("%d.%m.%Y")
deltaDay5 = (firstDayOfWeek - datetime.timedelta(days = 3)).strftime("%d.%m.%Y")
deltaDay6 = (firstDayOfWeek - datetime.timedelta(days = 2)).strftime("%d.%m.%Y")
deltaDay7 = (firstDayOfWeek - datetime.timedelta(days = 1)).strftime("%d.%m.%Y")

# Replace scel to vars
with open('tmp/xl/sharedStrings.xml', 'r') as file:
    filedata = file.read()
filedata = filedata.replace('dateFrom', deltaDay1)
filedata = filedata.replace('dateTo', deltaDay7)
filedata = filedata.replace('Date1', deltaDay1)
filedata = filedata.replace('date2', deltaDay2)
filedata = filedata.replace('Date3', deltaDay3)
filedata = filedata.replace('Date4', deltaDay4)
filedata = filedata.replace('Date5', deltaDay5)
filedata = filedata.replace('Date6', deltaDay6)
filedata = filedata.replace('Date7', deltaDay7)
with open('tmp/xl/sharedStrings.xml', 'w') as file:
    file.write(filedata)

# Make xlsx-file
shutil.make_archive('result', 'zip', 'tmp')
os.rename("result.zip", "MyName Отчет по выполнению работы в дистанционном режиме.xlsx")
shutil.rmtree('tmp')
