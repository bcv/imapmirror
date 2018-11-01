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

#exceptions=['Archive','Calendar','Outbox','Notes','History','Items','holidays','CS','IT']
exceptions=['CS']
mbox=[]
def printhelp():
	print("help")
	exit()

def printerror(strv):
	print("ERROR:",strv);
	exit()


if len(sys.argv) < 2:
	printhelp()


#print("Args:",sys.argv)
try:
 	opts,args = getopt.getopt(sys.argv[1:],"s:u:l:")
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


		

#print("To copy ",username,"@",servername," to ",localdir)

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
	fp=mailbox.mbox(fname)
	rv,data=M.search(None,"ALL")
	msglist=data[0].decode('utf-8').split()
	mboxformat="";
	for f in msglist:
		rv,mesg = M.fetch(f.encode('utf-8'),'(RFC822)')
		try:
			fp.add(mesg[0][1].decode('utf-8'))
			sys.stdout.write("!")
		except:
			sys.stdout.write(".")
		sys.stdout.flush()
	print("")

	



