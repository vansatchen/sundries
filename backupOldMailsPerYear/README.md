### This script for search and move old emails in dovecot maildir to dovecot namespace per year.
Requires installed *sendemail* because written on old mailserver with python3.4 with default ubuntu packages without pip and other thirdlevel packages.

## dovecot.conf
**Namespace in dovecot**
```
namespace {
    disabled = no
    hidden = no
    list = children
    ignore_on_failure = yes
    inbox = no
    location = maildir:/path/to/Archive/%Ld/%Ln/Maildir/.2020
    prefix = Archive_2020/
    subscriptions = yes
    separator = /
}
```

**Quota ignoring for archive**
```
quota_rule2 = Archive_*:ignore
```
