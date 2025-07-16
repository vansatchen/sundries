## What is this?
This script is used to allow mail delivery from other servers, but reject authorization from countries not on the list.
In this case, the list:
- RU - Russia
- BY - Belarus
- None - for local nets

## Install
Add to postfix:

**master.cf** to bottom:
```
geoip-check unix - n n - 0 spawn
    user=nobody argv=/etc/postfix/scripts/geoip-reject.py
```

**main.cf**
```
smtpd_relay_restrictions =
...
check_policy_service unix:private/geoip-check,
...
```
```
smtpd_client_restrictions =
    check_policy_service unix:private/geoip-check
    permit
```
