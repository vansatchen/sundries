#!/usr/bin/python3

# Add 'management localhost 7505' to openvpn server config

import telnetlib

HOST = "localhost"
PORT = "7505"

telnet = telnetlib.Telnet(HOST,PORT, 5)
telnet.write("status\n".encode("ascii"))
output = telnet.read_until("END\n".encode('utf-8'), 1).decode('ascii').split("\n")
telnet.close()

print('Common Name'.ljust(15), 'Real Address'.ljust(20), 'Virtual Address'.ljust(15), 'Bytes Received'.ljust(15), 'Bytes Sent'.ljust(15), 'Connected Since'.ljust(15))
for string in output:
    if 'CLIENT_LIST' in string and len(string.split(",")) == 13:
        print(string.split(",")[1].ljust(15), # Common Name
              string.split(",")[2].split(':')[0].ljust(20), # Real Address
              string.split(",")[3].ljust(15), # Virtual Address
              string.split(",")[5].ljust(15), # Bytes Received
              string.split(",")[6].ljust(15), # Bytes Sent
              string.split(",")[7].ljust(15)  # Connected Since
              )
