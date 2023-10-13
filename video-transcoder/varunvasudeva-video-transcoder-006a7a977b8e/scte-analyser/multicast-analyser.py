#!/usr/bin/python3

#Python application to analyse scte packets in transport stream and log the information.
#Varun Vasudeva
#Required: Python3 and threefive module 

import socket
import threefive
import struct
import io
from datetime import datetime
import json
import sys
import os

chname=sys.argv[1]
multicast_ip=sys.argv[2]
multicast_port=sys.argv[3]
scte_pid=sys.argv[4]
print(chname,multicast_ip,multicast_port,scte_pid)
#if '0x' in scte_pid: scte_pid=int(scte_pid, 16)

class TSScte35Parser():
	#Variable Declaration
	def __init__(self, mcast_ip,port,scte_pid,chname, if_ip="0.0.0.0", hostname="0.0.0.0"):
		self.HOST = hostname
		self.PORT = int(port)
		self.MCAST_IP = mcast_ip
		self.IF_IP = if_ip
		self.scte_pid = str(scte_pid)
		self.chname = chname

	def run(self):
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:	#creating socket
			self.set_socket_options(sock)	#socket options to listen multicast traffic
			sock.bind((self.HOST, self.PORT))
			with sock.makefile(mode="b") as socket_file:
				print('[Debug]Data Initiated')
				while True:
					try:
						scte = threefive.Stream(socket_file).decode_next()	#look for scte packet in transport stream
						if scte:	#if SCTE is true
							now = datetime.now()
							dt = now.strftime("%d/%m/%Y %H:%M:%S")
							DATE=now.strftime("%d%m%Y")
							scte_parser=json.loads(scte.get_json())
							scte_parser['packet_data']['date']=dt
							if str(scte_parser['packet_data']['pid']) == self.scte_pid:
								print('[Debug]SCTE FOUND')
								try:
									os.makedirs('logs')
								except:
									pass
								#writing logs to file
								f=open('logs/%s_tsanalyser_%s.log' % (chname,DATE),'a+')
								print(json.dumps(scte_parser)+'\n')
								f.write(json.dumps(scte_parser)+'\n')
								f.close()
						f_debug=open('logs/%s_tsanalyser_debug_%s.log' % (chname,DATE),'a+')
						now = datetime.now()
						dt = now.strftime("%d/%m/%Y %H:%M:%S")
						f_debug.write(dt+'\n')
						f_debug.write(scte.get_json()+'\n')
						f_debug.close()
					except Exception as e:
						print("[Debug]ERROR while decoding TS:", e)
						pass
	#socket options to listen to multicast data
	def set_socket_options(self, sock):
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(self.MCAST_IP)+socket.inet_aton(self.HOST))

if __name__ == "__main__":
	test = TSScte35Parser(multicast_ip,multicast_port,scte_pid,chname)
	test.run()
