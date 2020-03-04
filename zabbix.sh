#!/bin/bash

zurl="http://zabbix/zabbix/api_jsonrpc.php"
zuser=""
zpass=""
zpriority="3"
ztimefrom=$(date +%s --date="30 days ago")
zcount=0

# Get token
ztoken=$(curl --silent -H "Content-Type: application/json-rpc" -X POST $zurl -d '{"jsonrpc":"2.0","method":"user.login","params":{ "user":"'$zuser'","password":"'$zpass'"},"auth":null,"id":0}' | sed 's/{"jsonrpc":"2.0","result":"//g;s/","id":0}//g' )

# Get all problems
allProblems=$(curl --silent -H "Content-Type: application/json-rpc" -X POST $zurl -d '{"jsonrpc": "2.0","method": "problem.get","params": {"output": "extend","time_from": "'"$ztimefrom"'","sortorder": "ASC"},"auth": "'$ztoken'","id": 1}')
arrowProblem=$(echo $allProblems | awk 'BEGIN{RS=","}{print}')
for line in $arrowProblem
do
   zobjects=$(echo $line | grep "objectid" | sed 's/"//g;s/objectid://g')
   if [ -n "$zobjects" ]; then
      for zobject in $zobjects
      do
         zcount=$(( $zcount + 1 ))
         [ "$zcount" -ge "16" ] && break
         zproblem=$(curl --silent -H "Content-Type: application/json-rpc" -X POST $zurl -d '{"jsonrpc": "2.0","method": "event.get","params": {"output": "extend","selectHosts": "extend","objectids": "'$zobject'","sortfield": ["clock", "eventid"],"sortorder": "ASC"},"auth": "'$ztoken'","id": 1}')
         zhost=$(echo $zproblem | awk 'BEGIN{RS=","}{print}' | grep "host" | grep -v "hosts" | grep -v "hostid" | sed 's/"//g;s/host://g' | awk '(NR == 1)')
         zname=$(echo $zproblem | awk 'BEGIN{RS=","}{print}' | grep "name" | grep -v "ipmi_username" | sed 's/"//g;s/name://g' | awk '(NR == 1)' | sed 's/%/percent/g')
         [ -z "$zhost" ] && zhost="Unknown Host"
         [ -z "$zname" ] && zhost="Unknown Problem"
#         echo $zobject
#         echo $zhost
#         echo $zname
         /usr/bin/curl -d '{ "auth_token": "YOUR_AUTH_TOKEN", "title": "'"$zhost"'", "text": "'"$zname"'" }' http://dashing:3030/widgets/widget$zcount
      done
   fi
done
[ "$zcount" -le "15" ] || exit 0
zcount=$(( $zcount + 1 ))
for ((count=$zcount; count < 16; count++))
do
   /usr/bin/curl -d '{ "auth_token": "YOUR_AUTH_TOKEN", "title": ":::", "text": "---" }' http://dashing:3030/widgets/widget$count
done
