from conf import *
import time
from datetime import datetime
from sys import argv
import sys
from subprocess import PIPE, Popen

class aolControl():
	def __init__(self):
		self.rtmpURL=rtmpURL
	def checkRTMP(self):
		cmd0=f"timeout 8s ffprobe {self.rtmpURL}"
		p=Popen(cmd0, stdout=PIPE,stderr=PIPE,shell=True)
		p.wait()
		if(p.returncode != 0):
			return(False)
		else:
			return(True)
	def main(self):
		if(self.checkRTMP() is False):
			dt=datetime.now()
			print(f'{dt}: No input')
			cmd="/bin/bash aol-stream.sh stop"
			p=Popen(cmd,shell=True)
			p.wait()
			return(True)
		else:
			dt=datetime.now()
			print(f"{dt}: Input found, Starting Stream")
			cmd="/bin/bash aol-stream.sh start"
			p=Popen(cmd,shell=True)
			p.wait()
			return(True)
			
while True:
	try:
		p=aolControl()
		p.main()
		time.sleep(5)
	except KeyboardInterrupt:
		sys.exit()
	except Exception as e:
		print(e)
		continue