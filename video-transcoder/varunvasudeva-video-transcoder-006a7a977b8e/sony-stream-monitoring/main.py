from conf import *
from m3u8 import *
from subprocess import Popen, PIPE
from sys import argv
from os import makedirs
from datetime import datetime

class Downloader(object):
	def __init__(self,chname,url):
		self.url=url
		self.baseurl=url.split('?')[0].rsplit('/',1)[0]
		self.headers=headers
		self.chname=chname
		self.url=url
		self.output_path=output_path

	def split(self):
		cmd1=f"tmux split-window -t {self.chname} -v"
		p=Popen(cmd1,stdout=PIPE,stderr=PIPE,shell=True,close_fds=True)
		p.wait()
		cmd1=f"tmux select-layout -t {self.chname} tiled"
		p=Popen(cmd1,stdout=PIPE,stderr=PIPE,shell=True,close_fds=True)
		p.wait()
		return(True)

	def main(self):
		pl=load(self.url)
		cmd0=f"tmux kill-window -t {self.chname}"
		p=Popen(cmd0,stdout=PIPE,stderr=PIPE,shell=True,close_fds=True)
		p.wait()
		cmd0=f"tmux new-session -d -s {self.chname}"
		p=Popen(cmd0,stdout=PIPE,stderr=PIPE,shell=True,close_fds=True)
		p.wait()
		now = datetime.now()
		dt=now.strftime("%Y%m%d-%H%M")
		try:
			makedirs(f"{self.output_path}/{self.chname}/{dt}")
		except:
			pass
		i=0
		
		fMaster=open(f"{self.output_path}/{self.chname}/{dt}/master.m3u8",'a+')
		fMaster.write("#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-INDEPENDENT-SEGMENTS)")
		#print(pl.data['playlists'])
		for plData in pl.data['playlists']:
			uri=plData['uri']
			url=f"{self.baseurl}/{uri}"
			self.split()
			basename=url.split('?')[0].rsplit('/',1)[1]
			bandwidth=plData['stream_info']['bandwidth']
			avgbandwidth=plData['stream_info']['average_bandwidth']
			codecs=plData['stream_info']['codecs']
			resolution=plData['stream_info']['resolution']
			frame_rate=plData['stream_info']['frame_rate']
			fMaster.write(f"#EXT-X-STREAM-INF:BANDWIDTH={bandwidth},AVERAGE-BANDWIDTH={avgbandwidth},CODECS=\"{codecs}\",RESOLUTION={resolution},FRAME-RATE={frame_rate}\n")
			fMaster.write(f"{basename}\n")
			cmdURL=f"while true; do python3 monitor.py {self.chname} '{url}' {dt}; sleep .1; done"
			cmd0=f"tmux send-keys -t {self.chname}:0.{i} \"{cmdURL}\" C-m"
			print(cmd0)
			p=Popen(cmd0,stdout=PIPE,stderr=PIPE,shell=True,close_fds=True)
			p.wait()
			i+=1
		fMaster.close()
		print(url)
		
chname=argv[1]
url=argv[2]
s=Downloader(chname,url)
s.main()