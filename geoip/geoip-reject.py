#!/usr/bin/python3

import sys
import syslog
import re
import GeoIP

allowedCountry = [None, 'RU', 'BY']
attr = {}

syslog.openlog(ident="GeoIP", logoption=syslog.LOG_PID, facility=syslog.LOG_MAIL)
while True:
    data = sys.stdin.readline()
    m = re.match(r'([^=]+)=(.*)\n', data)
    if m:
        attr[m.group(1).strip()] = m.group(2).strip()
    else:
        clientAddress = attr['client_address']
        saslMethod = attr['sasl_method']
        sender = attr['sender']

        if saslMethod:
            gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
            countryCode = gi.country_code_by_addr(clientAddress)
            clientStr = " client_address = " + clientAddress + "; country = " + str(countryCode)
            if sender == 'spam@example.com' or countryCode not in allowedCountry:
                print("action=REJECT no connections accepted\n")
                syslog.syslog('Reject for ' + sender + ' with' + clientStr)
            else:
                print("action=DUNNO passed geoip check\n")
                syslog.syslog('Allow for ' + sender + ' with' + clientStr)
        else:
            # Dont use it for servers emails
            print("action=DUNNO passed geoip check\n")
        break

syslog.closelog()

#attr = {'client_name': 'somehost.example.com',
#        'request': 'smtpd_access_policy',
#        'protocol_name': 'ESMTP',
#        'queue_id': '',
#        'ccert_issuer': '',
#        'ccert_pubkey_fingerprint': '',
#        'reverse_client_name': 'somehost.example.com',
#        'protocol_state': 'RCPT',
#        'encryption_keysize': '256',
#        'instance': '9931.66431360.46390.4',
#        'etrn_domain': '',
#        'sasl_username': 'noreply@example.com',
#        'policy_context': '',
#        'encryption_cipher': 'ECDHE-RSA-AES256-SHA',
#        'ccert_fingerprint': '',
#        'recipient': 'otherhost@example.com',
#        'sender': 'Noreply@example.com',
#        'sasl_method': 'login',
#        'encryption_protocol': 'TLSv1',
#        'sasl_sender': '',
#        'stress': '',
#        'client_address': '10.158.40.133',
#        'recipient_count': '0',
#        'size': '0',
#        'ccert_subject': '',
#        'helo_name': 'somehost',
#        'client_port': '58637'}
