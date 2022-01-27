#!/usr/bin/python3

# Script that use for create and delete openVPN-users by group of Active Directory
# Dependencies: python3.4+, python3-ldap

import ldap
import os
import shutil
import subprocess
import zipfile
import shlex
import sys

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

ldapServer1 = "dc1.example.com"
ldapServer2 = "dc2.example.com" # Uses if ldapServer1 fail
ldapUser = "ldauser@example.com"
ldapPass = "ldapuserpass"
base = "OU=users,DC=example,DC=com"
scope = ldap.SCOPE_SUBTREE
filter = "(memberOf=CN=openvpn,OU=vpn,OU=Groups,DC=example,DC=com)"
attrs = ['sAMAccountName','mail']
resultSet = []
usersList = []
sumOfUsers = 0
sumOfVPNUsers = 0
ovpnDir = "/etc/openvpn/"
ccdPath = ovpnDir + "ccd/"
ovpnCA = ovpnDir + "easy-rsa/"
buildDir ="/opt/check4vpn/temp/"
smtpServer = "smtp.example.com"
fromAddr = "do-not-reply@example.com"
fromPass = "donotreplypass"

# Test connect to ldap-server
def testConnect(server):
    global lconn
    try:
        lconn = ldap.initialize('ldap://%s:389' % server)
        lconn.protocol_version = ldap.VERSION3
        lconn.set_option(ldap.OPT_REFERRALS, 0)
        lconn.simple_bind_s(ldapUser, ldapPass)
        return True
    except ldap.SERVER_DOWN:
        print("Error connection to %s" % server)
        return False

status = testConnect(ldapServer1)
if not status:
    status = testConnect(ldapServer2)
    if not status: sys.exit(1)

if not os.geteuid() == 0:
    sys.exit("\n\033[31mOnly root can run this script or try sudo\033[0m\n")

print("Ldap connection is OK\n=***=")

# Search for members in group
ldap_result_id = lconn.search_ext(base, scope, filter, attrs)

try:
    while 1:
      result_type, result_data = lconn.result(ldap_result_id, 0)
      if (result_data == []):
          break
      else:
          if result_type == ldap.RES_SEARCH_ENTRY:
              sumOfUsers += 1
              resultSet.append(result_data)
except ldap.SIZELIMIT_EXCEEDED:
    print()

# only for test
#resultSet.append([('CN=Testuser,OU=Users,DC=example,DC=com', {'mail': [b'testuser@example.com'], 'sAMAccountName': [b'testuser']})])
# only for test end

print("Users in group: %d" % sumOfUsers)
print("=***=\nChecking for configs")

# Cat file to file
def catFile(srcFileName, dstFileName):
    with open(srcFileName, "r") as srcFile:
        content = srcFile.read()
    with open(dstFileName, "a") as dstFile:
        dstFile.write(content)

# Func for send email
def sendMail(userMail, subject, message, filename):
    toAddr = userMail

    msg = MIMEMultipart()
    msg['From'] = fromAddr
    msg['To'] = toAddr
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))
    attach = ovpnCA + "keys/clients/" + filename
    attachment = open(attach, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)

    server = smtplib.SMTP(smtpServer, 587)
    server.starttls()
    server.login(fromAddr, fromPass)
    text = msg.as_string()
    server.sendmail(fromAddr, toAddr, text)
    server.quit()

# Parse users accounts from search request
for user in resultSet:
    userLogin = user[0][1].get("sAMAccountName")[0].decode("utf-8")
    if userLogin.endswith('$'):
        userLogin = userLogin[:-1]
    usersList.append(userLogin)
    if len(user[0][1]) < 2:
        userMail = False
    else:
        userMail = user[0][1].get("mail")[0].decode("utf-8")
    if not os.path.isfile(ccdPath + userLogin): # If user not in ccd path, generate config with keys
        print("New user \"%s\" detected" % userLogin)
        userScel = buildDir + userLogin + "/client.conf-skel"
        command = shlex.split("env -i bash -c 'cd /etc/openvpn/easy-rsa/; source ./vars; ./build-key --batch '" + userLogin)
        p = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p.communicate()
        if not os.path.exists(buildDir + userLogin): os.makedirs(buildDir + userLogin)
        shutil.copy(ovpnDir + "client.conf-skel", buildDir + userLogin)
        with open(userScel, "a") as file: file.write('<ca>\n')
        catFile(ovpnCA + "keys/ca.crt", userScel)
        with open(userScel, "a") as file: file.write('</ca>\n')
        with open(userScel, "a") as file: file.write('<cert>\n')
        catFile(ovpnCA + "keys/" + userLogin + ".crt", userScel)
        with open(userScel, "a") as file: file.write('</cert>\n')
        with open(userScel, "a") as file: file.write('<key>\n')
        catFile(ovpnCA + "keys/" + userLogin + ".key", userScel)
        with open(userScel, "a") as file: file.write('</key>\n')
        os.rename(userScel, userLogin + ".conf")
        shutil.copy(userLogin + ".conf", userLogin + ".ovpn")
        # Zip configs to zipfile
        with zipfile.ZipFile(buildDir + userLogin + "/" + userLogin + ".zip", 'w') as zipConf:
            zipConf.write(userLogin + ".conf")
            zipConf.write(userLogin + ".ovpn")
        os.replace(buildDir + userLogin + "/" + userLogin + ".zip", ovpnCA + "keys/clients/" + userLogin + ".zip")
        shutil.rmtree(buildDir + userLogin, ignore_errors=True)
        os.remove(userLogin + ".conf")
        os.remove(userLogin + ".ovpn")
        # Send email
        if userMail:
            # Generate gender tittle
            userLen = len(user[0][0].split(",")[0].split("=")[1].split())
            if userLen != 3:
                gender = "Ув."
                userIO = user[0][0].split(",")[0].split("=")[1]
            else:
                userIO = user[0][0].split(",")[0].split("=")[1].split(" ", 1)[1]
                gender = "Уважаемая" if userIO[-2:] == "на" else "Уважаемый"

            subject = "Файл конфигурации для openvpn"
            message = "%s %s.\nРаспакуйте архив в директорию openvpn.\n"\
                      "Это письмо сгенерировано автоматически. Пожалуйста, не отвечайте на него." % (gender, userIO)
            filename = userLogin + ".zip"
            sendMail(userMail, subject, message, filename)
            sendMail('ovpn-admins@example.com', subject, message, filename)
        else:
            subject = "Mail " + userLogin + " is not set in Active Directory"
            message = "Please, set it. Config for openvpn sended only for admins."
            sendMail('ovpn-admins@example.com', subject, message, userLogin + '.zip')
        # Generate ccd file for new user
        with open(ccdPath + userLogin, "w") as file:
            file.write('push "route 10.0.0.0 255.255.255.0"')

print("=***=\nSearching for deleted users")
vpnUsers = os.listdir(ccdPath)
for vpnUser in vpnUsers: sumOfVPNUsers += 1
print("=***=\nVPN users in ccd: %s" % sumOfVPNUsers)
for vpnUser in vpnUsers: # Search removed users from group
    if not vpnUser in usersList:
        print("User %s not in VPN group, removing." % vpnUser)
        os.remove(ccdPath + vpnUser)
        command = shlex.split("env -i bash -c 'cd /etc/openvpn/easy-rsa/; source ./vars; ./revoke-full '" + vpnUser)
        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        shutil.copy(ovpnCA + "keys/crl.pem", ovpnDir + "crl.pem")

print("Done.")
