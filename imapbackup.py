#!/usr/bin/env python3


#Author:Bhasker C V(bhasker@unixindia.com)
#GNU GPL v2


#Very simple programme to mirror a IMAP server contents here with
# minimal inputs given (just the required ones).


import sys, getopt,os;
import imaplib,mailbox;
import getpass,re;

servername=""
username=""
localdir=""
replacefile=False

exceptions=[]  #Folder names you do not want to be synced. TODO: add this to input options ?
mbox=[]
def printhelp():
	print("-s <server name/ip> -u <user name>  -l <local directory>  -r <flag to set replace of a MDIR(default append)")
	print("Output:")
	print(" ! => Success \n . => Erroe ")
	exit()

def printerror(strv):
	print("ERROR:",strv);
	exit()


if len(sys.argv) < 2:
	printhelp()


#print("Args:",sys.argv)
try:
 	opts,args = getopt.getopt(sys.argv[1:],"rs:u:l:")
except:
	printhelp()


#print(len(opts))
for opt, arg in opts:
	if opt == "-s":
		servername=arg
	if opt == "-u":
		username=arg
	if opt == "-l":
		localdir=arg
		if not re.search('[/]$',localdir):
			localdir=localdir+'/'
	if opt == "-r":
		replacefile=True


		

#print("To copy ",username,"@",servername," to ",localdir)

ignfil = open(os.getenv("HOME")+"/.imap-ignore","r")
ignlist = ignfil.read().split('\n')

#Start ...

M = imaplib.IMAP4_SSL(servername)

try:
	rv, data = M.login(username,getpass.getpass())
except imaplib.IMAP4.error:
	printerror("Error logging into IMAP")

if rv != 'OK':
	printerror("Login failed. Wrong password ? ")

rv,mlist= M.list()

for f in mlist:
	mbox.append((' '.join((re.search("[)] .*",f.decode('utf-8'))).group(0).split()[2:])).replace('"',''))

for mailfolder in mbox:
	mailfoldername=mailfolder
	if any(mailfoldername in s for s in ignlist):
		continue

	print("Processing ",mailfoldername)
	rv,tot=M.select('"'+mailfolder+'"')
	try:
		if int(tot[0]) > 0:
			print("Folder:"+mailfoldername+" has "+str(int(tot[0]))+" messages")
		else:	
			continue
	except:
		print("Error processing mailbox:"+mailfoldername)
		continue

#	os.chdir(localdir)
	fname=mailfoldername
	if any(fname in s for s in exceptions):
		continue
	if not os.path.isdir(os.path.dirname(fname)) and re.search('[/]',fname):
#		print("processing:"+fname)
		mdirname=os.path.dirname(fname)+'/'
		mdirname='.dir/'.join(mdirname.split('/'))
#		print("need to create "+mdirname)
		fulllocaldirname=localdir+'/'+mdirname
		if not os.path.exists(fulllocaldirname):
			os.makedirs(fulllocaldirname)
		fname=mdirname+"/"+os.path.basename(fname)
		fname=localdir+fname
#		print("Final Filename to create:"+fname)
	else:
		fname=localdir+fname
	#fp=open(fname,"w+")
	if replacefile and os.path.exists(fname):
		os.remove(fname)
	fp=mailbox.mbox(fname,create=True)
	rv,data=M.search(None,"ALL")
	msglist=data[0].decode('utf-8').split()
	mboxformat="";
	for f in msglist:
		rv,mesg = M.fetch(f.encode('utf-8'),'(RFC822)')
		try:
			fp.add(mesg[0][1])
			sys.stdout.write("!")
		except:
			sys.stdout.write(".")
		sys.stdout.flush()
	print("")

	



