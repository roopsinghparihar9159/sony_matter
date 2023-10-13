import sys
from time import sleep,strptime
from subprocess import Popen, PIPE, run
import os
import re
import json
from datetime import datetime
import requests
from dbconn import *
from conf import *

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
		self.apiURL="https://www.ptivideos.com/pti/live-clips"

	def getTime(self):
		now = datetime.now()
		date=now.strftime("%Y-%m-%d %H:%M:%S")
		return(date)

	def hwdevice(self):				#Return which GPU device process should use(incase of 'auto' only)
		cards=['0','2']
		usage=[]
		for i in cards:
			cmd="nvidia-smi dmon -i %s -c 1 | tail -n 1| awk '{s=$7+$8}END{print s}'" % (i)
			p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
			out,err=p.communicate()
			out=int(out)
			usage.append(out)
		return usage.index(min(usage))

	def genThumb(self,fn):
		title=fn.split('/')[-1].split('-')[0]
		basefn=fn.split('/')[-1].split('.')[0]
		DTS=basefn.split('-')[1].split('_')[0]
		fn=f"{self.storage_dir}/{fn}"
		output_dir=f"{self.output_dir}/clips/{title}/{DTS}"
		cmd="ffmpeg -y -i %s -f image2 -vframes 1 %s/thumb.png" % (fn,output_dir)
		print(cmd)
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		if(p.returncode != 0):
			print(f"{self.getTime()} - Thumbnail Generation Failed")
			return(False)
		else:
			print(f"{self.getTime()} - Thumbnail Generated")
			return(True)

	def getDuration(self,fn):
		fn=f"{self.storage_dir}/{fn}"
		cmd=f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -sexagesimal {fn}"
		#print(cmd)
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		if(err.decode('utf-8') != ''):
			print(err)
		out=out.decode('utf-8').strip()
		return(out.rstrip())

	def getMeta(self,fn):
		cmd="ffprobe -v quiet -show_streams -print_format json \"%s/%s\"" % (self.storage_dir,fn)
		#print(cmd)
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		metadata=json.loads(out)
		for data in metadata['streams']:
			if(data['codec_type'] == 'video'):
				fps=str(data['r_frame_rate']).replace('/1','')
				codec_name=data['codec_name']
		print(f"FPS: {fps}, Codec: {codec_name}")
		return(fps,codec_name)

	def transcoder(self,fn):
		status='Ok'
		interlace_opts=''
		basefn=fn.split('/')[-1].split('.')[0]
		DTS=basefn.split('-')[1].split('_')[0]
		title=basefn.split('-')[0]
		#basefn=re.sub(r"[\(\)]",'',basefn)
		fps,codec_name=self.getMeta(fn)
		gop=str(int(fps)*2)
		#interlace_opts=" -drop_second_field 0 "
		hwdevice=self.hwdevice()
		print(f"Using NVidia: {hwdevice}")
		input_opts="-hwaccel_device %s" % (hwdevice)
		#cmd="FFREPORT=file=logs/%s.log:level=32 ffmpeg -y %s %s -async 1 -vsync 1 -i \"%s/%s\"  " % (basefn,input_opts,interlace_opts,self.storage_dir,fn)
		cmd=f"ffmpeg -y -async 1 -vsync 1 -i \"%s/%s\""
		ttl_flavors=len(self.transcode_profile)
		ttl_flavors+=1
		filter_opts=" -filter_complex \"[0:v]format=nv12,split=%s" % (ttl_flavors)
		count=1
		filter_scale_opts=""
		split_opts=""
		transcode_opts=""
		try:
			os.makedirs(f"{self.output_dir}/clips/{title}/{DTS}")
		except Exception as e:
			#print(e)
			pass
		#mp4Files=[]
		for flavor in self.transcode_profile:
			split_opts+="[s_v%s]" % (count)
			vbitrate=flavor.split('|')[0]
			res=flavor.split('|')[1]
			abitrate=flavor.split('|')[2]
			vcrop=flavor.split('|')[3]
			vidType=flavor.split('|')[4]
			mrate=int(vbitrate)
			#mrate=int(vbitrate)*10
			if(vcrop == '0'):
				filter_scale_opts+="[s_v%s]scale=%s,format=yuv420p,hwupload_cuda[out%s];" % (count,res,count)
			else:
				filter_scale_opts+="[s_v%s]scale=%s:force_original_aspect_ratio=increase,crop=%s[out%s];" % (count,res,res,count)
			op_fn=f"{self.output_dir}/clips/{title}/{DTS}/{DTS}_{vidType}.mp4"
			#print(op_fn)
			#mp4Files.append(op_fn)
			transcode_opts+=" -map \"[out%s]\" -c:v libx264 -r:v %s -g:v %s -b:v %s -maxrate %s -preset:v fast -metadata service_provider=multitv -metadata service_name=multitv -map 0:a -c:a aac -b:a %s -ar 48000 %s " % (count,fps,gop,vbitrate,mrate,abitrate,op_fn)
			count+=1
		filter_scale_opts=filter_scale_opts[:-1]
		filter_opts+=" %s;%s\"" % (split_opts,filter_scale_opts)
		cmd+=filter_opts
		cmd+=transcode_opts
		print(f"Transcoding Logs: logs/{basefn}.log")
		#print(cmd)
		#sys.exit()
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		#print(out,err)
		if(p.returncode != 0):
			status="FF-Failed"
		else:
			status="Ok"
		print(f"{self.getTime()} - Transcoding completed, Status={status}")
		self.genThumb(fn)

		cur,db=dbconn()
		now = datetime.now()
		completed_dt = now.strftime("%Y-%m-%d %H:%M:%S")
		cur.execute(f"update ptirecoder set status='1',completed_dt='{completed_dt}',duration='00:05:00.00' where filename='{fn}';")
		db.commit()
		db.close()
		return(status)

	def main(self):
		cur,db=dbconn()
		cur.execute("select filename from ptirecoder where status='0' and type='c' limit 0,1;")
		try:
			fn=cur.fetchone()[0]
		except Exception as e:
			print(f"{self.getTime()} - Nothing to Do")
			db.close()
			return(False)
		db.close()
		#print(fn)
		cur,db=dbconn()
		cur.execute(f"update ptirecoder set status='-1' where filename='{fn}';")
		db.commit()
		db.close()
		if('_clips' in fn):
			self.transcoder(fn)


"""s=Read_Xfer()
s.main()"""
while True:
	try:
		s=Read_Xfer()
		s.main()
		sleep(10)
	except KeyboardInterrupt:
		sys.exit()
	except Exception as e:
		print(e)
		continue