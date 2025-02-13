#!/usr/bin/python3

# Testing
# curl "http://localhost/cgi-bin/clickToCall.py?phone=XXXXXXX&exten=XXXX"

import telnetlib
import time
import cgi

args = cgi.FieldStorage()

HOST = "127.0.0.1"
PORT = "5038"
user = "user"
password = "userPass"
context = "context"
exten = args["exten"].value # src
toNum = args["phone"].value.replace(' ', '').replace('-', '') # dst
if toNum.startswith('7'): toNum = '8' + toNum[1:]

with telnetlib.Telnet(HOST,PORT) as tn:
    tn.write("Action: login\n".encode('ascii'))
    tn.write(f"Username: {user}\n".encode('ascii'))
    tn.write(f"Secret: {password}\n\n".encode('ascii'))

    tn.write("Action: Originate\n".encode('ascii'))
    tn.write(f"Channel: Local/{exten}@{context}\n".encode('ascii'))
    tn.write(f"Exten: {toNum}\n".encode('ascii'))
    tn.write("Context: {context}\n".encode('ascii'))
    tn.write("Priority: 1\n".encode('ascii'))
    tn.write("Async: yes\n".encode('ascii'))
    tn.write("WaitTime: 15\n".encode('ascii'))
    tn.write(f"Callerid: {toNum}\n\n".encode('ascii'))

    time.sleep(1)

print('Content-type:text/html\n\n')
