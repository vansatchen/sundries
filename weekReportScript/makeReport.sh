#!/bin/bash

# Simle script makes report in xlsx file for remote job
# Developed by vansatchen

# Check date arg exists and valid
[ -z "$1" ] && echo "Usage: makeReport.sh currentDate (example:20210525)" && exit 1
if [ $(echo $1 | wc -c) -le 8 ] || [ $(echo $1 | wc -c) -ge 10 ]; then
	echo "Invalid date"
	exit 1
fi

# Check date valid
dateYear=$(echo ${1:0:4}) 
[ ${dateYear:0:3} != 202 ] && echo "Invalid YEAR" && exit 1
dateMonth=$(echo ${1:4:2})
[ "$dateMonth" -gt 12 ] && echo "Invalid MONTH" && exit 1
dateDay=$(echo ${1:6:2})
[ "$dateDay" -gt 31 ] && echo "Invalid DAY" && exit 1

# Calculate first day of week
dayOfWeek=$(date -d $1 +%u)
firstDayOfWeek=$(date -d "$1 $(($dayOfWeek - 1)) days ago" +%Y%m%d)

# Make report xlsx
cp -r ./scel tmp
day1=$(date -d "$firstDayOfWeek 7 days ago" +%d.%m.%Y)
day2=$(date -d "$firstDayOfWeek 6 days ago" +%d.%m.%Y)
day3=$(date -d "$firstDayOfWeek 5 days ago" +%d.%m.%Y)
day4=$(date -d "$firstDayOfWeek 4 days ago" +%d.%m.%Y)
day5=$(date -d "$firstDayOfWeek 3 days ago" +%d.%m.%Y)
day6=$(date -d "$firstDayOfWeek 2 days ago" +%d.%m.%Y)
day7=$(date -d "$firstDayOfWeek 1 days ago" +%d.%m.%Y)
sed -i "s/dateFrom/$day1/g" tmp/xl/sharedStrings.xml
sed -i "s/dateTo/$day7/g" tmp/xl/sharedStrings.xml
sed -i "s/Date1/$day1/g" tmp/xl/sharedStrings.xml
sed -i "s/date2/$day2/g" tmp/xl/sharedStrings.xml
sed -i "s/Date3/$day3/g" tmp/xl/sharedStrings.xml
sed -i "s/Date4/$day4/g" tmp/xl/sharedStrings.xml
sed -i "s/Date5/$day5/g" tmp/xl/sharedStrings.xml
sed -i "s/Date6/$day6/g" tmp/xl/sharedStrings.xml
sed -i "s/Date7/$day7/g" tmp/xl/sharedStrings.xml
cd tmp
zip -r ../$firstDayOfWeek\ MyName\ Отчет\ по\ выполнению\ работы\ в\ дистанционном\ режиме.xlsx *
cd ..
rm -rf tmp

exit 0
