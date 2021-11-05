#!/usr/bin/python3

# Make phonebook for ip-phones in xml format
# Works with asterisk pjsip mysql db.

import MySQLdb

pbLocation = "/var/www/html/phonebook/phonebook.xml"

db = MySQLdb.connect(user="asteriskuser", passwd="asteriskpass", host="127.0.0.1", db="asteriskdb", charset='utf8')
cursor = db.cursor()
cursor.execute("select id, callerid from ps_endpoints")
data = cursor.fetchall()

with open(pbLocation, "w") as file:
    file.write('<?xml version="1.0" encoding="UTF-8"?>\n<AddressBook>\n')

for row in data :
    formatRow1 = row[1].split("<")[0]
    number = row[0]
    if number == "2999": continue  # exclude unwanted numbers
    lastName = formatRow1.split()[0]
    try:
        firstName = formatRow1.split()[1]
    except IndexError:
        firstName = ""

    with open(pbLocation, "a") as file:
        file.write("  <Contact>\n")
        file.write("    <FirstName>%s</FirstName>\n" % (lastName))
        file.write("    <LastName>%s</LastName>\n" % (firstName))
        file.write("        <Phone>\n")
        file.write("      <phonenumber>%s</phonenumber>\n" % (number))
        file.write("      <accountindex>1</accountindex>\n")
        file.write("      <downloaded>1</downloaded>\n")
        file.write("    </Phone>\n")
        file.write("    <Groups>\n")
        file.write("      <groupid>2</groupid>\n")
        file.write("    </Groups>\n")
        file.write("  </Contact>\n")

with open(pbLocation, "a") as file:
    file.write("</AddressBook>\n")

db.close()
