import hashlib
import os
from datetime import datetime
import sys


userid = raw_input("\nPlease enter User ID:\n")
userid = userid.strip()
password = raw_input("\nPlease enter password for User " + userid + ":\n")
password = hashlib.md5(password.encode()).hexdigest()


if os.path.isfile('password'): 
	with open('password') as f:
		allusers = zip(*[line.split() for line in f])[0]

	if userid in allusers:
		print "User already exists"
		sys.exit(0)

with open('password', 'a') as file:
	file.write(userid + " " + password + " " + str(datetime.now()) + "\n")

