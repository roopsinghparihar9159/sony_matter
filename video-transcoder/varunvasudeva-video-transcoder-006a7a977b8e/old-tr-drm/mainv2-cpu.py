import requests
from subprocess import PIPE, Popen, run
from datetime import datetime
import json
import DownloadProgressBar
import logging
import os, shlex
from sys import exit,argv
from time import sleep

class transcoder(object):
	def __init__(self):
		self.base="/opt"
		self.apiCallbackBase="https://creator.multitvsolution.com"
		self.apiCallback=f"{self.apiCallbackBase}/crons/drm_transcode"
		self.apiStatusUpdate=f"{self.apiCallbackBase}/crons/transcodeupdate"
		logging.basicConfig(filename="logs/transcode.log", format='%(asctime)s %(message)s',filemode='a+')
		self.logger = logging.getLogger()
		self.logger.setLevel(logging.DEBUG)
	
	def getMeta(self,fn):
		cmd=f"ffprobe -v quiet -show_streams -print_format json \"{fn}\""
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		metadata=json.loads(out)
		for data in metadata['streams']:
			if(data['codec_type'] == 'video'):
				fps=str(data['r_frame_rate'])
				if('/' in fps):
					calc_fps=float(fps.split('/')[0])/float(fps.split('/')[1])
					fps="%.2f" % calc_fps
				codec_name=data['codec_name']
				try:
					duration=data['duration']
				except:
					duration='0'
		#print(fps,codec_name,duration)
		return(fps,codec_name,duration)
	
	def downloadFile(self,fn,downloadFn):
		#downloadFn=fn.split('/')[-1]
		self.logger.debug(f"Downloading {fn} as {downloadFn}")
		try:
			DownloadProgressBar.download_url(fn,downloadFn)
		except:
			pass
	
	def statusUpdate(self,map_id,content_id,status):
		data = {'id': map_id, 'content_id': content_id, 'status': status}
		p=requests.post(self.apiStatusUpdate,data=data)
		print(p.text)

	def main(self):
		apiCallback_r=requests.get(self.apiCallback)
		jsonData=json.loads(apiCallback_r.content)
		try:
			if(jsonData['error'] == 'No record found'):
				print(jsonData['error'])
				return(False)
		except:
			pass
		transcode_opts=''
		video_file_path=jsonData[0]['content_id'][-1]['video_file_name']
		fn=jsonData[0]['content_id'][-1]['name']
		map_id=jsonData[0]['content_id'][-1]['map_id']
		content_id=jsonData[0]['content_id'][-1]['content_id']
		print(content_id)
		self.statusUpdate(map_id,content_id,'inprocess')
		#if( not os.path.exists(fn)):
		video_file_path = video_file_path.replace(' ','%20')
		print(f"Downloading {video_file_path}")
		self.downloadFile(video_file_path,fn)
		try: fps,codec_name,duration=self.getMeta(f"{fn}")
		except: fps=0
		if(fps == 0): 
			self.statusUpdate(map_id,content_id,'error')
			print('QC Failed')
			return(True)
		fileSize = str(round(int(os.path.getsize("%s" % (fn)))/1024/1024))
		input_opts=" -vsync 1 -async 1 "
		mp4files=''
		for data in jsonData[0]['content_id']:
			vbitrate=data['vb']
			vbitrate=vbitrate.replace('k','000')
			mrate=int(vbitrate)*5
			if(mrate > 10000000): mrate="16000000"
			ab=data['ab']
			resolution=data['screen']
			width,height=resolution.split('x')
			content_id=data['content_id']
			video_file_path=data['video_file_name']
			video_file_name=data['name']
			basefn=video_file_name.split('.')[0]
			flavor_name=data['flavor_name']
			watermark_logo=data['watermark_logo']
			watermark_pos=data['watermark_pos']
			bucket=data['bucket']
			map_id=data['map_id']
			site_id=data['site_id']
			access_key=data['access_key']
			drm_cid=data['drm_cid']
			app_id=data['app_id']
			cfURL=data['cloudfront']
			gop=float(fps)*2
			gop="%.2f" % gop
			op_dir=f"{content_id}/mp4/{basefn}"
			op_fn=f"{op_dir}/{basefn}_{vbitrate}.mp4"
			try: os.makedirs(f"{op_dir}")
			except: pass
			#scale_opts="-vf scale_cuda=w=%s:h=%s" % (width,height)
			scale_opts=f" -s {width}x{height}"
			transcode_opts+=f" -map \"0:v\" -c:v libx264 -r:v {fps} -g:v {gop} -b:v {vbitrate} -maxrate {mrate} -preset:v veryfast {scale_opts} -force_key_frames 'expr:gte(t,n_forced*2)' -metadata service_provider=multitv -metadata service_name=multitv -map 0:a -c:a aac -b:a {ab} -ar 48000 {op_fn} "
			mp4files+=' '+op_fn
		print(mp4files)
		#cmd=f"FFREPORT=file=logs/{video_file_name}.log:level=32 ffmpeg -y {input_opts} -async 1 -vsync 1 -i '{fn}'  "
		cmd=f"ffmpeg -y {input_opts} -async 1 -vsync 1 -i '{fn}'  "
		cmd=f"{cmd}{transcode_opts}"
		run(shlex.split(cmd))
		#awscmd=f"aws s3 cp {op_dir} s3://{bucket}/multitv/video/{op_dir} --recursive --acl public-read --output json"
		#run(shlex.split(awscmd))
		#os.system('aws s3 cp '+travod_path+' s3://'+bucket+'/multitv/video/'+travod_path+' --recursive --acl public-read')
		print(f"PallyConPackager --site_id {site_id} --access_key {access_key} --content_id {drm_cid} --dash --hls -i {mp4files} -o {content_id}")
		packagingCmd=f"PallyConPackager --site_id {site_id} --access_key {access_key} --content_id {drm_cid} --dash --hls -i {mp4files} -o {content_id}"
		#run(shlex.split('/app/PallyCon-Packager-Cloud-v3.8.1/bin/Linux/PallyConPackager --site_id '+site_id+' --access_key '+access_key+' --content_id '+drm_cid+' --dash --hls -i {mp4files} -o '+content_id+' '))
		run(shlex.split(packagingCmd))
		#rmcommand=f"rm -rf {content_id}/mp4"
		#run(shlex.split(rmcommand))
		drmUploadCmd=f"aws s3 cp {content_id} s3://{bucket}/multitv/video/{content_id} --recursive --acl public-read"
		run(shlex.split(drmUploadCmd))
		dash=f"{cfURL}/multitv/video/{content_id}/dash/stream.mpd"
		hls=f"{cfURL}/multitv/video/{content_id}/hls/master.m3u8"
		data={'id': map_id, 'content_id': content_id, 'hls': hls, 'dash': dash, 'duration' : duration, 'hls_size': fileSize}
		print(data)
		r=requests.post('https://creator.multitvsolution.com/crons/drm_tanscoded_url', data=data)
		print(r.text)
		rmcommand=f"rm -rf {content_id} {fn}"
		run(shlex.split(rmcommand))
		
while True:
	try:
		s=transcoder()
		if(s.main() is False): sleep(10)
	except KeyboardInterrupt:
		exit()
	except:
		continue