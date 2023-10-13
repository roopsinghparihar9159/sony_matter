from conf import *
import requests
import hashlib
import time
from sys import argv
import xmltodict
import sys
from subprocess import PIPE, Popen

class elementalControl():
	def __init__(self,eventID,action):
		self.eventID=eventID
		self.action=action
		self.eleIp=eleIp
		self.eleUser=eleUser
		self.eleKey=eleKey
		self.url=f"http://{self.eleIp}"

	def create_key(self,uri):
		epoch=str(int(time.time()+60))
		api_auth_key=hashlib.md5(("%s%s%s%s" % (uri,self.eleUser,self.eleKey,epoch)).encode('utf-8')).hexdigest()
		api_auth_key=hashlib.md5(("%s%s" % (self.eleKey,api_auth_key)).encode('utf-8')).hexdigest()
		return(api_auth_key,epoch)

	def elementalHandlerPost(self,uri):
		api_auth_key,epoch=self.create_key(uri)
		url=f"{self.url}{uri}"
		header={"Accept":"application/xml","Content-type":"application/xml","X-Auth-User":self.eleUser,"X-Auth-Expires":epoch,"X-Auth-Key":api_auth_key}
		r=requests.post(url, headers=header)
		return(r.text)

	def elementalHandlerGet(self,uri):
		api_auth_key,epoch=self.create_key(uri)
		url=f"{self.url}{uri}"
		header={"Accept":"application/xml","Content-type":"application/xml","X-Auth-User":self.eleUser,"X-Auth-Expires":epoch,"X-Auth-Key":api_auth_key}
		r=requests.get(url, headers=header)
		return(r.text)

	# def elementalHandlerInputSw(self,uri,inputLabel):
	# 	api_auth_key,epoch=self.create_key(uri)
	# 	url=f"{self.url}{uri}"
	# 	header={"Accept":"application/xml","Content-type":"application/xml","X-Auth-User":self.eleUser,"X-Auth-Expires":epoch,"X-Auth-Key":api_auth_key}
	# 	data=f"<input_label>{inputLabel}</input_label> "
	# 	r=requests.post(url, headers=header, data=data)
	# 	return(r.text)

	def main(self):
		uri=f"/live_events/{self.eventID}/status"
		eleData=xmltodict.parse(self.elementalHandlerGet(uri))
		streamStatus=eleData['live_event']['status']
		print(streamStatus)
		if(streamStatus != 'running'):
			uri=f"/live_events/{self.eventID}/reset"
			self.elementalHandlerPost(uri)
		uri=f"/live_events/{self.eventID}/{self.action}"
		self.elementalHandlerPost(uri)
		uri=f"/live_events/{self.eventID}/reset"
		self.elementalHandlerPost(uri)

eventID=341
action= 'stop' #argv[0]
print('eventID',eventID,'','action',action)
p=elementalControl(eventID,action)
p.main()
time.sleep(5)

# p = elementalControl()
uri1 = 'http://103.253.175.106'
result = p.create_key(uri1)
print(result)