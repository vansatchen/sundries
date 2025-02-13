## cgi-bin script allowing make call via Asterisk Click2Call extension for Google Chrome

### Step 1.
Add a new manager to /etc/asterisk/manager.conf on your Asterisk box.
```
[user]
secret=userPass
writetimeout=100
read=system,call,log,verbose,command,agent,user,config,originate
write=system,call,log,verbose,command,agent,user,config,originate
```
### Step 2.
Copy clickToCall.py to /var/cgi-bin

### Step 3.
Test it:
```
curl "http://localhost/cgi-bin/clickToCall.py?phone=XXXXXXX&exten=XXXX"
```

### Step 4.
Install [Asterisk Click2Call](https://chromewebstore.google.com/detail/asterisk-click2call/hlnmjkbpmnbgeondjeceaomhafdacmlj?hl=hy)

### Step 5.
Update the extension settings. You have to set up your Asterisk extension and AMI script's URL. Then click Save button.
 
### Step 6.
You're done! To make a call from the web brower just highlight the phone number you want to dial, make a right click and choose Call context menu. Asterisk will do the rest.

### Step 7.
You can set up basic authentication on the web server to protect your script. In this case use Username and Password fields to provide the credentials.

### Step 8.
To make a replacement like +7 -> 8 in phone numbers use Replace characters field. The syntax is a|b (replace all occurrences of a with b in dialed numbers). Special characters must be escaped with backslash. Several rules must be separated by commas. Keep in mind that all non-digit characters will be removed before the call processed regardless of this setting, so you don't need to replace brackets and dashes here.
