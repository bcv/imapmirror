# imapmirror
Mirrors IMAP server data into local mbox tree
A simple(in my opinion) and easy method to create a mirror of IMAP into a local mbox tree

imapbackup.py  

options:

-s : server name of IMAP server / IP

-u : user name for logging into the server (password will be prompted)

-l : top of the directory under which the mbox is populated

thats it ! 
sit back and observe

Uses cisco style output 
Each message when downloaded shows 
! -> success
. -> Failed

**Please note: This is in NO WAY a fool proof code. This script is pre-alpha. **
