import sys
from time import sleep,strptime
from subprocess import Popen, PIPE, run
import shlex
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
		title=fn.split('-')[1]
		basefn=fn.split('/')[-1].split('.')[0]
		fn=f"{self.storage_dir}/{fn}"
		output_dir=f"{self.output_dir}/{title}"
		cmd="ffmpeg -y -i %s -f image2 -vframes 1 %s/thumb.png" % (fn,output_dir)
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		if(p.returncode != 0):
			print(f"{self.getTime()} - Thumbnail Generation Failed")
			return(False)
		else:
			print(f"{self.getTime()} - Thumbnail Generated")
			return(True)

	def upload(self,uploadDir,basefn):
		basefn=basefn.split('/')[-1].split('.')[0]
		print(basefn)
		appID=basefn.split('_')[0]
		title=basefn.split('-')[1]
		#cmd="/usr/local/bin/aws s3 sync %s s3://%s/events/recording//%s/" % (uploadDir,self.bucketName,baseFn)
		cmd=f"/usr/local/bin/aws s3 sync {uploadDir}/ s3://{self.bucketName}/events/recording/{appID}/{title}/"
		print(cmd)
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		err=err.decode('utf-8')
		if(err != ''):
			return(False)
		else:
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
		cmd="ffprobe -v quiet -show_streams -print_format json \"%s/%s\"" % (self.input_dir,fn)
		#print(cmd)
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		metadata=json.loads(out)
		for data in metadata['streams']:
			if(data['codec_type'] == 'video'):
				print(data['r_frame_rate'])
				fps=str(int(data['r_frame_rate'].replace('/1','').replace('\n','')))
				codec_name=data['codec_name']
		print(f"FPS: {fps}, Codec: {codec_name}")
		return(fps,codec_name)

	def transcoder(self,fn):
		status='Ok'
		interlace_opts=''
		basefn=fn.split('/')[-1].split('.')[0]
		title=basefn.split('-')[1]
		#basefn=re.sub(r"[\(\)]",'',basefn)
		fps,codec_name=self.getMeta(fn)
		gop=str(int(fps)*2)
		#interlace_opts=" -drop_second_field 0 "
		#hwdevice=self.hwdevice()
		input_opts="-hwaccel_device 2"
		#cmd="FFREPORT=file=logs/%s.log:level=32 ffmpeg -y %s %s -async 1 -vsync 1 -i \"%s/%s\"  " % (basefn,input_opts,interlace_opts,self.storage_dir,fn)
		cmd=f"ffmpeg -y -async 1 -vsync 1 -i {self.input_dir}/{fn}"
		ttl_flavors=len(self.transcode_profile)
		ttl_flavors+=1
		filter_opts=" -filter_complex \"[0:v]format=nv12,split=%s" % (ttl_flavors)
		count=1
		filter_scale_opts=""
		split_opts=""
		transcode_opts=""
		try:
			os.makedirs(f"{self.output_dir}/{title}")
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
				filter_scale_opts+="[s_v%s]scale=%s,format=yuv420p[out%s];" % (count,res,count)
			else:
				filter_scale_opts+="[s_v%s]scale=%s:force_original_aspect_ratio=increase,crop=%s[out%s];" % (count,res,res,count)
			op_fn=f"{self.output_dir}/{title}/{title}_{vidType}.mp4"
			#print(op_fn)
			#mp4Files.append(op_fn)
			transcode_opts+=" -map \"[out%s]\" -c:v libx264 -r:v %s -g:v %s -b:v %s -maxrate %s -preset:v ultrafast -metadata service_provider=multitv -metadata service_name=multitv -map 0:a -c:a aac -b:a %s -ar 48000 %s " % (count,fps,gop,vbitrate,mrate,abitrate,op_fn)
			count+=1
		filter_scale_opts=filter_scale_opts[:-1]
		filter_opts+=" %s;%s\"" % (split_opts,filter_scale_opts)
		cmd+=filter_opts
		cmd+=transcode_opts
		print(f"Transcoding Logs: logs/{basefn}.log")
		#print(cmd)
		#sys.exit()
		run(shlex.split(cmd))
		"""p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		#print(out,err)
		if(p.returncode != 0):
			status="FF-Failed"
		else:
			status="Ok" """
		print(f"{self.getTime()} - Transcoding completed, Status={status}")
		self.genThumb(fn)
		upload=self.upload(f"{self.output_dir}/{title}",basefn)
		if(upload == True):
			##PTI1_6566-demo_1-1674128269.flv
			appID=basefn.split('_')[0]
			content_id=basefn.split('_')[1].split('-')[0]
			title=basefn.split('-')[1]
			DTS=basefn.split('-')[2].split('.')[0]
			Data=[]
			val={}
			val['SOURCE_URL_HD']=f"{self.cdnURL}/events/recording/{appID}/{title}/{title}_HD.mp4"
			val['SOURCE_URL_SD']=f"{self.cdnURL}/events/recording/{appID}/{title}/{title}_SD.mp4"
			val['SOURCE_URL_LOW']=f"{self.cdnURL}/events/recording/{appID}/{title}/{title}_lowres.mp4"
			val['SOURCE_URL_THUMBNAIL']=f"{self.cdnURL}/events/recording/{appID}/{title}/thumb.png"
			val['content_id']=content_id
			val['DURATION']=self.getDuration(fn)
			val['content_title']=title
			val['TIME_STAMP']=DTS
			Headers={"Content-Type": "application/json"}
			#Data=[{'SOURCE_URL_HD': '%s','SOURCE_URL_SD': '%s','SOURCE_URL_LOW': '%s','SOURCE_URL_THUMBNAIL': '%s','content_id': '%s','content_title': '%s','TIME_STAMP':'%s','DURATION':'%s'}] % (hdUrl,sdUrl,lowresUrl,thumbUrl,content_id,title,DTS,duration)
			Data.append(val)
			print(Data)
			r=requests.post(self.apiURL, headers=Headers, data=json.dumps(Data))
			print(f"Response Code: {r.status_code}")
			print(r.text)
			cur,db=dbconn()
			now = datetime.now()
			completed_dt = now.strftime("%Y-%m-%d %H:%M:%S")
			#print(f"update ptirecoder set status='1',completed_dt='{completed_dt}',duration='{val['DURATION']}' where filename='{fn}';")
			cur.execute(f"update ptirecoder set status='1',completed_dt='{completed_dt}',duration='{val['DURATION']}' where filename='{fn}';")
			db.commit()
			db.close()
		return(status)

	def main(self):
		cur,db=dbconn()
		cur.execute("select filename from ptirecoder where status='0' and type='r' limit 0,1;")
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
		self.transcoder(fn)


s=Read_Xfer()
s.main()
"""while True:
	try:
		s=Read_Xfer()
		s.main()
		sleep(10)
	except KeyboardInterrupt:
		sys.exit()
	except Exception as e:
		print(e)
		continue"""