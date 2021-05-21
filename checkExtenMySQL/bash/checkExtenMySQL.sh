#!/bin/bash

userdb=asteriskuser
passdb=asteriskpass
database=asteriskdb
dbhost=127.0.0.1
tabledb=ps_contacts
idcolumn="id"
addrcolumn="via_addr"
mysqlconnect="mysql -h $dbhost -u $userdb -p$passdb -D $database"

checkid=`$mysqlconnect -B -N -e "select $addrcolumn from $tabledb where id like '%$1%';" 2>/dev/null | sed 's/ //g'`
if [ ! -z "$checkid" ]; then
#	resultat="Call to local EXTEN"
	resultat="PJSIP/$1"
else
#	resultat="Call to old ATC"
	resultat="OOH323/old-ats-h323/$1"
fi

/bin/echo "SET VARIABLE checkNumVar \"$resultat\""
