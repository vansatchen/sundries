#!/usr/bin/python3

import subprocess, os, shutil

archYear = 2020
userDomain = 'example.com'
userPath = '/path/to/maildir/users/' + userDomain + '/'
archPath = '/path/to/Archive/' + userDomain + '/'
archYearNewer = str(archYear + 1)
mailSubject = 'Внимание. Произведено архивирование сообщений вашего почтового аккаунта'

def archiveMails(user):
    user = user + '/'
    findCommand = "find " + userPath + user + " ! -name 'dovecot*' ! -name 'maildirfolder' ! -name 'subscriptions' ! -name 'managesieve.sieve' -type f ! -newermt " + "'jan 01 " + archYearNewer + "'"
    result = subprocess.check_output(findCommand, shell=True)
    mailCount = 0
    for line in result.decode('utf8').split('\n'):
        if line:
            lineWOPath = line.replace(userPath + user, '').replace('Maildir/', '').split('/')
            mail = lineWOPath[-1:][0]
            pathToMail = '/'.join(lineWOPath[:-1])
            pathToArch = archPath + user + 'Maildir/' + '.' + str(archYear) + '/' + pathToMail
            os.makedirs(pathToArch, exist_ok=True)
            mailToArch = userPath + user + 'Maildir/' + pathToMail + '/' + mail
            try:
                shutil.move(mailToArch, pathToArch)
            except:
                print("Cannot archive file ", mailToArch)
            # adding current directory to subscriptions
            subscriptionsFile = archPath + user + 'Maildir/' + '.' + str(archYear) + '/subscriptions'
            if not os.path.isfile(subscriptionsFile):
                with open(subscriptionsFile, 'a') as f:
                    f.close()
            else:
                with open(subscriptionsFile, 'r+') as f:
                    subscriptionText = pathToMail.replace('.', '').replace('/cur', '')
                    if subscriptionText not in f.read():
                        f.write(subscriptionText + "\n")

            mailCount += 1

    # Move emails from cur/ to directory named Inboxmails
    dirOfYear = archPath + user + 'Maildir/' + '.' + str(archYear)
    if os.path.isdir(dirOfYear):
        inboxFiles = os.listdir(dirOfYear)
        if 'cur' in inboxFiles:
            os.makedirs(dirOfYear + '/.Inboxmails', exist_ok=True)
            try:
                shutil.move(dirOfYear + '/cur', dirOfYear + '/.Inboxmails/')
            except:
                print("Cannot archive directory ", dirOfYear + '/cur')
            with open(subscriptionsFile, 'r+') as f:
                f.write('Inboxmails\n')

    doveadmCommand = '/usr/bin/doveadm quota recalc -u ' + user[:-1] + '@' + userDomain
    status = subprocess.Popen(doveadmCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
    if status == 0 and mailCount > 0:
        print(user[:-1], mailCount)
        sendEmailCommand = '/usr/bin/sendemail -q -f doNotReply@example.com -xu doNotReply@example.com -xp examplePass -t ' + \
                           user[:-1] + '@' + userDomain + \
                           ' -o message-charset=utf-8 -u "' + mailSubject + \
                           '" -m "В директорию Archive_' + str(archYear) + ' перемещены все сообщения за ' + str(archYear) + \
                           ' год в количестве: ' + str(mailCount) + '" -s mail.example.com'
        subprocess.Popen(sendEmailCommand, shell=True)


allEmails = sorted(os.listdir(userPath))
allEmails = ['someuser'] # For testing
for i in allEmails:
    if os.path.isdir(userPath + i):
        archiveMails(i)
