#!/bin/bash

# Make phonebook for ip-phones in xml format
# Works with asterisk pjsip mysql db.

userdb=asteriskuser
passdb=asteriskpass
database=asteriskdb
dbhost=127.0.0.1
tabledb=ps_endpoints
mysqlconnect="mysql -h $dbhost -u $userdb -p$passdb -D $database"
pbLocation="/path/to/phonebook/phonebook.xml"

getAccounts=$($mysqlconnect -B -N -e "select id, callerid from ps_endpoints;" 2> /dev/null)

echo '<?xml version="1.0" encoding="UTF-8"?>' > $pbLocation
echo '<AddressBook>' >> $pbLocation

while read -r line; do
    number=$(echo "$line" | awk '{print $1}')
    lastName=$(echo "$line" | awk '{print $2}' | sed -e 's/<.*//g')
    firstName=$(echo "$line" | awk '{print $3}' | sed -e 's/<.*//g')
    [[ "$number" == "2999" ]] && continue # exclude unwanted numbers

cat <<EOF >> $pbLocation
  <Contact>
    <FirstName>$lastName</FirstName>
    <LastName>$firstName</LastName>
    <Phone>
      <phonenumber>$number</phonenumber>
      <accountindex>1</accountindex>
      <downloaded>1</downloaded>
    </Phone>
    <Groups>
      <groupid>2</groupid>
    </Groups>
  </Contact>
EOF

done <<< "$getAccounts"

echo '</AddressBook>' >> $pbLocation
