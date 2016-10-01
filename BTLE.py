#!/bin/python

import time
from scapy.all import *
import os
import sys
import code
import argparse
from threading import Thread
import gevent
from binascii import unhexlify
import subprocess

# Create Connection with default parameters
def Connect(BT_conn, addr, random):
	HCI_packet_type = "01"
	createleconn = "0D20"
	param_length = "19"
	scan_interval = "6000"
	scan_window = "3000"
	init_filter = "00"
	peer_addr = random
	BD_addr = addr
	own_addr = "00"
	conn_interval_min = "2800"
	conn_interval_max = "3800"
	conn_latency = "0000"
	supv_timeout = "2A00"
	min_CE = "0000"
	max_CE = "0000"

	raw = HCI_packet_type + createleconn + param_length + scan_interval + scan_window + init_filter + \
	peer_addr + BD_addr + own_addr + conn_interval_min + conn_interval_max + conn_latency + supv_timeout + min_CE + max_CE

	print("Connected")

	raw = bytearray.fromhex(raw)
	BT_conn.send(raw)
	time.sleep(.5)
	return BT_conn

# Create Connection with specific parameters
def Cust_Connect(BT_conn, addr, random, scan_int, scan_win, own_address, conn_int_min, conn_int_max, supv_time):
	HCI_packet_type = "01"
	createleconn = "0D20"
	param_length = "19"
	scan_interval = scan_int
	scan_window = scan_win
	init_filter = "00"
	peer_addr = random
	BD_addr = addr
	own_addr = own_address
	conn_interval_min = conn_int_min
	conn_interval_max = conn_int_max
	conn_latency = "0000"
	supv_timeout = supv_time
	min_CE = "0000"
	max_CE = "0000"

	raw = HCI_packet_type + createleconn + param_length + scan_interval + scan_window + init_filter + \
	peer_addr + BD_addr + own_addr + conn_interval_min + conn_interval_max + conn_latency + supv_timeout + min_CE + max_CE

	print("Connected")

	raw = bytearray.fromhex(raw)
	BT_conn.send(raw)
	time.sleep(.3)
	return BT_conn

# Write Request
def writereq(s, handle, value):
	# ACL Packet header
	HCI_packet_type = "02"
	ACL_packet = "4000"
	data_length = ""
	L2CAP_length = ""
	L2CAP_prot = "0400"
	opcode = "12"

	# Set L2CAP and Data lengths
	L2CAP_l = (int(len(value)) + 6)/2

	if len(value) < 18:
		data_length = "0" + str2hex((len(value) + 14)/2) + "00"
		L2CAP_length = "0" + str2hex(L2CAP_l) + "00"

	elif 18 <= len(value) < 50:
		data_length = str2hex((len(value) + 14)/2) + "00"
		L2CAP_length = "0" + str2hex(L2CAP_l) + "00"
		if len(value) > 26:
			L2CAP_length = str2hex(L2CAP_l) + "00"
	
	elif 50 < len(value):
		data_length = str2hex((len(value) + 14)/2) + "0"
		L2CAP_length = str2hex(L2CAP_l) + "00"
		if 58 < len(value):
			L2CAP_length = str2hex(L2CAP_l) + "0"

	else:
		data_length = "0" + str2hex((len(value) + 14)/2) + "00"
		L2CAP_length = "0" + str2hex(L2CAP_l) + "00"

	raw = HCI_packet_type + ACL_packet + data_length + L2CAP_length + L2CAP_prot + opcode + handle + value
	print("Writing " + value + " to handle: " + handle)
	raw = bytearray.fromhex(raw)
	s.send(raw)
	time.sleep(.3)

# convert integer to string(hex) in correct format (0x0001 -> 01)
def str2hex(value):
	hexvalue = str('{0:x}'.format(int(value)))
	return hexvalue

# Disconnect
def disconnect(s):
	raw = "01060403400013"
	raw = bytearray.fromhex(raw)
	s.send(raw)
	print("Disconnected")

def prepwrite(s, offset, handle, value):
	# ACL Packet header
	HCI_packet_type = "02"
	ACL_packet = "4000"
	data_length = ""
	L2CAP_length = ""
	L2CAP_prot = "0400"
	opcode = "16"

	# Set L2CAP and Data lengths (needs implementation like write req)
	L2CAP_l = (int(len(value)) + 10)/2

	if len(value) > 14:
		data_length = str2hex((len(value) + 18)/2) + "00"
		if len(value) > 22:
			L2CAP_length = str2hex(L2CAP_l) + "00"
	else:
		data_length = "0" + str2hex((len(value) + 18)/2) + "00"
		L2CAP_length = "0" + str2hex(L2CAP_l) + "00"

	raw = HCI_packet_type + ACL_packet + data_length + L2CAP_length + L2CAP_prot + opcode + handle + offset + value
	print(raw)
	raw = bytearray.fromhex(raw)
	s.send(raw)
	time.sleep(.3)

def execwrite(s):
	# ACL Packet header
	HCI_packet_type = "02"
	ACL_packet = "4000"
	data_length = "0600"
	L2CAP_length = "0200"
	L2CAP_prot = "0400"
	opcode = "18"
	value = "01"

	raw = HCI_packet_type + ACL_packet + data_length + L2CAP_length + L2CAP_prot + opcode + value
	print(raw)
	raw = bytearray.fromhex(raw)
	s.send(raw)
	time.sleep(.3)

def bindsock():
	output = subprocess.check_output(['bash','-c', "hciconfig hci0 down"])
	BT_conn = BluetoothUserSocket()
	return BT_conn
	time.sleep(.5)

def spoof(BT_conn, BD_addr):
	raw = bytearray.fromhex("01011000")
	BT_conn.send(raw)

	change_addr = "0101fc06" + BD_addr
	raw = bytearray.fromhex(change_addr)
	BT_conn.send(raw)

	raw = bytearray.fromhex("01030c00")
	BT_conn.send(raw)
	time.sleep(.3)

def switchrole(BT_conn, BD_addr):
	role = "01"

	change_role = "010b0807" + BD_addr + role
	raw = bytearray.fromhex(change_role)
	BT_conn.send(raw)
	time.sleep(.3)

def exMTUreq(BT_conn,size):
	# change MTU
	MTU = "02400007000300040002" + size
	raw = bytearray.fromhex(MTU)
	BT_conn.send(raw)
	time.sleep(.3)

def conn_oriented_chan(BT_conn, data):
	HCI_packet_type = "02"
	ACL_packet = "4000"
	data_length = "1b00"
	L2CAP_length = "1700"
	L2CAP_prot = "0401"

	raw = HCI_packet_type + ACL_packet + data_length + L2CAP_length + L2CAP_prot + data
	print(raw)
	raw = bytearray.fromhex(raw)
	BT_conn.send(raw)
	time.sleep(.3)

def readreq(BT_conn, handle):
	read = "0240000700030004000a" + handle
	raw = bytearray.fromhex(read)
	BT_conn.send(raw)
	time.sleep(.3)

	# Write Request
def writecmd(s, handle, value):
	# ACL Packet header
	HCI_packet_type = "02"
	ACL_packet = "4000"
	data_length = ""
	L2CAP_length = ""
	L2CAP_prot = "0400"
	opcode = "52"

	# Set L2CAP and Data lengths
	L2CAP_l = (int(len(value)) + 6)/2

	if len(value) < 18:
		data_length = "0" + str2hex((len(value) + 14)/2) + "00"
		L2CAP_length = "0" + str2hex(L2CAP_l) + "00"

	elif 18 <= len(value) < 50:
		data_length = str2hex((len(value) + 14)/2) + "00"
		L2CAP_length = "0" + str2hex(L2CAP_l) + "00"
		if len(value) > 26:
			L2CAP_length = str2hex(L2CAP_l) + "00"
	
	elif 50 < len(value):
		data_length = str2hex((len(value) + 14)/2) + "0"
		L2CAP_length = str2hex(L2CAP_l) + "00"
		if 58 < len(value):
			L2CAP_length = str2hex(L2CAP_l) + "0"

	else:
		data_length = "0" + str2hex((len(value) + 14)/2) + "00"
		L2CAP_length = "0" + str2hex(L2CAP_l) + "00"

	raw = HCI_packet_type + ACL_packet + data_length + L2CAP_length + L2CAP_prot + opcode + handle + value
	print("Writing " + value + " to handle: " + handle)
	raw = bytearray.fromhex(raw)
	s.send(raw)
	time.sleep(.3)