#!/bin/bash

txtbd="/var/lib/asterisk/documentation/text.txt"
calleridnum="$1"

[ -z "$calleridnum" ] && calleridname="anonymous"
[ $(echo ${#calleridnum}) = 4 ] && calleridnum=${calleridnum:1}

chechcid=$(/bin/grep -w "$calleridnum" $txtbd | /usr/bin/awk -F";" '{print $1}')
if [ -z "$chechcid" ]; then
	calleridname="$calleridnum"
else
	calleridname="$chechcid"
fi

/bin/echo "SET VARIABLE calleridvar \"$calleridname\""

