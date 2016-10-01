#!/bin/python

# Unlock Elecycle Smart Lock
# Uses "encrypted" communication but the commands never change once the password is established

import time
import subprocess
import struct
import os
import binascii
import threading
import signal
import socket
from scapy.all import *
from BTLE import *

def main():
	#s = bindsock()

	output = subprocess.check_output(['bash','-c', "hciconfig hci0 down"])
	s = BluetoothUserSocket()

	LEsetscanparam(s, "01")
	LEsetscan(s, "01", "00")
	BD_Addr = []

	while not keystop():
		try:
			data = None
			data = s.recv()
			data = str(data).encode("hex")

			addr = data[14:26]
			addr = ":".join(reversed([addr[i:i+2] for i in range(0, len(addr), 2)]))
			

			if data[2:4] == "3e":
				if data[10:12] == "04":
					if data[36:38] == "08":
						data_length = (int(data[34:36],16) - 1)*2
						name = data[38:38+data_length].decode("hex")
						if addr not in BD_Addr:
							print addr + "   " + name
							BD_Addr.append(addr)

					if data[30:32] == "09":
						data_length = (int(data[28:30],16) - 1)*2
						name = data[32:32+data_length].decode("hex")
						if addr not in BD_Addr:
							print addr + "   " + name
							BD_Addr.append(addr)

				elif data[10:12] == "00":
					length = int(data[34:36],16)*2
					if data[38+length:40+length] == "08":
						data_length = (int(data[36+length:38+length],16) - 1)*2
						name = data[40+length:40+data_length+length].decode("hex")
						if addr not in BD_Addr:
							print addr + "   " + name
							BD_Addr.append(addr)

					elif data[38+length:40+length] == "09":
						data_length = (int(data[36+length:38+length],16) - 1)*2
						name = data[40+length:40+data_length+length].decode("hex")
						if addr not in BD_Addr:
							print addr + "   " + name
							BD_Addr.append(addr)

				else:
					if addr not in BD_Addr:
						print addr + "   " + "Unknown"
						BD_Addr.append(addr)



											# elif data[36:38] == "02":
					# 	if data[44:46] == "08":
					# 		data_length = (int(data[42:44],16) - 1)*2
					# 		name = data[46:46+data_length].decode("hex")
					# 		if addr not in BD_Addr:
					# 			print addr + "   " + name
					# 			BD_Addr.append(addr)
					# 	elif data[44:46] == "09":
					# 		data_length = (int(data[42:44],16) - 1)*2
					# 		name = data[46:46+data_length].decode("hex")
					# 		if addr not in BD_Addr:
					# 			print addr + "   " + name
					# 			BD_Addr.append(addr)
					

				# if data[10:12] == "02":
					# print data[10:12]


							#print data[82:84] + "\n"


			# for line in data.splitlines():
			# 	if "HCI_Event_Hdr  code=0x3e" in line:
			# 		#print line

			# 		for part in line.split():
			# 			if "addr=" in part:
			# 				addr = part[5:22]

			# 			# if "data=" in part:
			# 			# 	for data in line.split("\'"):
			# 			# 		print line
			# 			# 		print data
			# 		i = loc.find("t")
			# 		print i

						# if "data=" in part:
						# 	loc = part[5:]
						# 	if "t" in loc:
						# 		i = loc.index("t")
						# 		# print i
						# 		data_length = part[i+2:i+4]
						# 		#if "t" in part[5:]:
						# 		try:
						# 			data_length = int(data_length,16)
						# 			if addr not in BD_Addr:
						# 				print addr + "    " + part[i+6:i+5+data_length]
						# 				BD_Addr.append(addr)

						# 		except ValueError:
						# 			break
		except KeyboardInterrupt:
			print "\nExiting"
			LEsetscan(s, "00", "00")
			disconnect(s)
			sys.exit()
			return() 

def keystop(delay = 0):
	return len(select.select([sys.stdin], [], [], delay)[0])

if __name__ == "__main__":
	while not keystop():
		try:
			main()
		except KeyboardInterrupt:
			print "\n Exiting"
		except IndexError:
			print "Error: Index"
		finally:
			sys.exit()