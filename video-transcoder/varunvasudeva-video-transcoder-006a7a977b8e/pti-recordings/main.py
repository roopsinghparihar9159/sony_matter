import sys
from time import sleep,strptime
from subprocess import Popen, PIPE
import os
import re
import json
from datetime import datetime
import requests
from conf import *
from dbconn import *
import time

class Read_Xfer(object):
	def __init__ (self):
		self.logfile='/var/log/xferlog'
		self.transcode_profile=["500000|720:480|96k|0|lowres","1500000|720:576|96k|1|SD","2500000|1920:1080|128k|0|HD"]
		self.storage_dir="/storage/FTP/PTI"
		self.input_dir=f"{self.storage_dir}/input"
		self.output_dir=f"{self.storage_dir}/output" 
		self.aws_access_key_id="AKIASTLI4S4OMLEZ2L6T"
		self.aws_secret_access_key="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"
		self.bucketName="pti-octopus"
		self.cdnURL="https://d36tipha2ffni.cloudfront.net"
		self.apiURL="https://ptivideos.com/pti/live-clips"

	def follow(self,file):
		file.seek(0,2)
		while True:
			line = file.readline()
			if not line:
				sleep(0.1)
				continue
			return(yield line)

	def getTime(self):
		now = datetime.now()
		date=now.strftime("%Y-%m-%d %H:%M:%S")
		return(date)

	def main(self):
		logdata=open(self.logfile,'r')
		loglines=self.follow(logdata)
		for line in loglines:
			line_data=line.split()
			#print(line_data)
			status=line_data[-1].strip()
			direction=line_data[11]
			user=line_data[13]
			if(status == 'c') and (user == 'pti') and (direction == 'i'):
				#print(line,status)
				fn=line_data[8].split('/')[-1]
				print(f"Received {fn}")
				chno=fn.split('_')[0]
				#self.transcoder(fn)
				if '_clips' in fn:
					ftype='c'
				else:
					ftype='r'
					cmd0=f"rm -rf /var/www/html/clips/{chno}/1*"
					print(cmd0)
					p=Popen(cmd0,stdout=PIPE,stderr=PIPE,shell=True)
					out,err=p.communicate()
					print(out,err)
				now = datetime.now()
				arrival_time = now.strftime("%Y-%m-%d %H:%M:%S")
				cur,db=dbconn()
				cur.execute(f"insert into ptirecoder(filename,status,arrival_dt,type) values('{fn}','0','{arrival_time}','{ftype}');")
				db.commit()
				db.close()

		logdata.close()

"""s=Read_Xfer()
s.main()"""
while True:
	try:
		s=Read_Xfer()
		s.main()
	except KeyboardInterrupt:
		sys.exit()
	except Exception as e:
		print(e)
		continue