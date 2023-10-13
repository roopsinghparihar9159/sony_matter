from conf import *
from m3u8 import *
from sys import argv,exit
import requests
import DownloadProgressBar
import base64
from Crypto.Cipher import AES
from datetime import datetime
from os import makedirs,path
from time import sleep, time
from shutil import copy

class monitor(object):
	def __init__(self,chname,url,time):
		self.url=url
		self.basepath=url.split('?')[0].rsplit('/',1)[0]
		self.basename=url.split('?')[0].rsplit('/',1)[1]
		self.output_path=output_path
		self.headers=headers
		self.chname=chname
		self.time=time

	def decode(self,obj):
		base64_bytes = base64.b64encode(obj)
		return(base64_bytes)

	def int2bytes(self,val):
		val="{:032x}".format(val)
		return(bytes.fromhex(val))

	def main(self):
		#now = datetime.now()
		#dt=now.strftime("%Y%m%d-%H%M")
		dt=self.time
		output_path=f"{self.output_path}/{self.chname}/{dt}"
		try:
			makedirs(output_path)
		except:
			pass 
		#print(self.url)
		m3u8name=f"{self.url}".split('?')[0].split('/')[-1]
		tempm3u8=f"{output_path}/.{m3u8name}.tmp"
		f=open(f"{tempm3u8}",'w+')
		m3u8init="#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-TARGETDURATION:4\n"
		f.write(m3u8init)
		f.close()
		while True:
			outpl=load(f"{output_path}/.{m3u8name}.tmp")
			s = requests.Session()
			req=s.get(self.url, headers=headers)
			#print(req.status_code)
			s.close()
			req = requests.request("GET", self.url, headers=self.headers)
			pl=loads(req.text)
			#print(req.status_code)
			data=pl.data
			#print(data)
			targetduration=data['targetduration']
			mediaSequence=data['media_sequence']
			Sequence=self.int2bytes(mediaSequence)
			for segmentData in data['segments']:
				#print(segmentData)
				uri=segmentData['uri']
				duration=segmentData['duration']
				#print(uri.split('?')[0].split('/')[-1])
				filename=uri.split('?')[0]
				filepath=filename.rsplit('/',1)[0]
				filename=filename.split('/')[-1]
				try:
					makedirs(f"{output_path}/{filepath}")
				except:
					pass
				video_file_path=f"{self.basepath}/{uri}"
				rkey=requests.get(segmentData['key']['uri'], headers=headers)
				key=rkey.content
				cipher = AES.new(key, AES.MODE_CBC,iv=Sequence)
				if( not path.exists(f"{output_path}/{filepath}/{filename}")):
					print(f"{output_path}/{filepath}/{filename}")
					with open(f"{output_path}/{filepath}/{filename}", 'wb') as seg_ts:
						for chunk in requests.request(url=video_file_path, stream=True, headers=headers, method="get"):
							seg_ts.write(cipher.decrypt(chunk))
					f=open(f"{tempm3u8}",'a+')
					f.write(f"#EXTINF:{duration},\n{filepath}/{filename}\n")
					f.close()
					copy(f"{tempm3u8}",f"{output_path}/{m3u8name}")
				mediaSequence+=1
				Sequence=self.int2bytes(mediaSequence)
			sleep(targetduration)
		
chname=argv[1]
url=argv[2]
time=argv[3]
s=monitor(chname,url,time)
s.main()