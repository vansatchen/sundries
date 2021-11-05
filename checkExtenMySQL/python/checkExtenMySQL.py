#!/usr/bin/python3

# Use with asterisk for route calls by connected ip-phones.
# Call user by PJSIP if phone registered, or route to analog ATC.

import MySQLdb
import sys

if len(sys.argv) < 2:
    sys.exit(1)
else:
    argNum = sys.argv[1]

db = MySQLdb.connect(user="asteriskuser",passwd="asteriskpass",host="127.0.0.1",db="asteriskdb")
cursor = db.cursor()
cursor.execute("select via_addr from ps_contacts where id like '%" + argNum + "%'")
data=cursor.fetchall()

if data:
    resultat = "PJSIP/" + argNum
else:
    resultat = "OOH323/panasonic-h323/" + argNum

print("SET VARIABLE checkNumVar \"" + resultat + "\"")

db.close()
