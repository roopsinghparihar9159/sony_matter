from email.mime import base
from dbconn import *
from conf import *
import os, sys
import boto3
from subprocess import PIPE, Popen, run
import shlex
from datetime import datetime
from time import sleep
import json
import m3u8
import botocore
import re,DownloadProgressBar

class transcode(object):
	def __init__(self):
		self.logfile=transcode_log
		if(os.path.exists(f"{self.logfile}") is True):
			os.makedirs(f"{self.logfile}")
   
	def getTime(self):
		now = datetime.now()
		date=now.strftime("%Y-%m-%d %H:%M:%S")
		return(date)

	def genThumb(self,output_dir,basefn,fn):
		cmd="ffmpeg -y -i %s -s 384x216 -f image2  -s 384x216  -vframes 1 %s/hls/%s/master.png" % (fn,output_dir,basefn)
		print(cmd)
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		if(p.returncode != 0):
			print(f"{self.getTime()} - Thumbnail Generation Failed")
			return(False)
		else:
			print(f"{self.getTime()} - Thumbnail Generated")
			return(True)

	def getFile(self):
		cur,db=dbconn()
		cur.execute("select dt,bucketname,path,qc,isTranscoded,filename from s3transcoder where qc='0' limit 0,1;")
		dbData=cur.fetchone()
		#print(dbData)
		if(dbData is not None): 
			dt,bucketName,filePath,qc,isTranscoded,fn=dbData
		else:
			db.close()
			print(f"{self.getTime()} - Nothing to Do")
			return(False)
		db.close()
		try:
			os.makedirs("%s/mp4" % output_dir)
			os.makedirs("%s/hls" % output_dir)
			os.makedirs(download_dir)
		except:
			pass
		print(f"{self.getTime()} - Downloading s3://{bucketName}/{filePath}/{fn}")
		cur,db=dbconn()
		cur.execute(f"update s3transcoder set qc='-1' where filename='{fn}';")
		db.commit()
		db.close()
		# s3 = boto3.resource('s3',aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
		# bucket=s3.Bucket(bucketName)
		downloadFn=f"{download_dir}/{fn}"
		video_file_path = f"https://d36tipha2ffni.cloudfront.net/{filePath}/{fn}"
		print(f"Downloading {video_file_path} as {downloadFn}")
		try:
			# bucket.download_file(f"{filePath}/{fn}",downloadFn)
			DownloadProgressBar.download_url(video_file_path,downloadFn)
		except Exception as e:
			print(e)
			cur,db=dbconn()
			cur.execute(f"update s3transcoder set qc='err',isTranscoded='err' where filename='{fn}';")
			db.commit()
			db.close()
			return(False)
		"""s3 = boto3.client('s3')
		s3.download_file(bucketName, filePath, fn)"""
		print(f"{self.getTime()} - Downloaded s3://{bucketName}/{filePath}/{fn}")
		sleep(1)
		print(downloadFn)
		if(os.path.exists(downloadFn) is True):
			print(fn)
			return(fn)
		else:
			return(False)

	def sortPlaylist(self,masterfn):
		srcf=open(masterfn,'r')
		playlist_text=srcf.read()
		srcf.close()
		parsed_playlist = m3u8.loads(playlist_text)
		parsed_playlist.playlists.sort(key=lambda x: x.stream_info.average_bandwidth)
		new_playlist_text = parsed_playlist.dumps()
		f=open(masterfn,'w+')
		f.write(new_playlist_text)
		f.close()
		return(True)

	def upload(self,uploadFn,baseFn,fn):
		s3 = boto3.client('s3')
		cur,db=dbconn()
		cur.execute(f"select bucketname from s3transcoder where filename='{fn}'")
		bucketName=cur.fetchone()[0]
		cmd="/usr/local/bin/aws s3 sync %s s3://%s/HLS/%s/" % (uploadFn,bucketName,baseFn)
		print(cmd)
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		err=err.decode('utf-8')
		"""cmd="/usr/local/bin/aws s3 cp /data/transcoder/mp4/%s_4000000.mp4 s3://%s/mp4/%s_HD.mp4" % (baseFn,bucketName,baseFn)
		print(cmd)
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		err=err.decode('utf-8')"""
		cmd=f"/usr/local/bin/aws s3 cp {output_dir}/mp4/{baseFn}_2200000.mp4 s3://{bucketName}/mp4/{baseFn}_SD.mp4"
		print(cmd)
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		err=err.decode('utf-8')	
		if(err != ''):
			return(False)
		else:
			return(True)

	def qc(self,fn):
		downloadFn=f"{download_dir}/{fn}"
		cmd="ffmpeg -v error -i \"%s\" -codec copy -f null -" % (downloadFn)
		print(f"{self.getTime()} - Analyzing {fn}")
		p=Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
		out,err=p.communicate()
		if(err.decode('utf-8') == ''):
			qc='Ok'
		else:
			qc='Failed'
		cur,db=dbconn()
		cur.execute(f"update s3transcoder set qc='{qc}' where filename='{fn}';")
		print(f"{self.getTime()} - QC {qc}")
		db.commit()
		db.close()
		return(True)

	def getMeta(self,fn):
		cmd="ffprobe -v quiet -show_streams -print_format json \"%s/%s\"" % (download_dir,fn)
		print(cmd)
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		metadata=json.loads(out)
		for data in metadata['streams']:
			if(data['codec_type'] == 'video'):
				fps=str(data['r_frame_rate']).replace('/1','')
				codec_name=data['codec_name']
		print(fps,codec_name)
		return(fps,codec_name)

	def transcoder(self):
		status='Ok'
		interlace_opts=''
		cur,db=dbconn()
		cur.execute("select dt,bucketname,path,qc,isTranscoded,filename from s3transcoder where isTranscoded='0' and qc='Ok' and isUploaded='0' limit 0,1;")
		dbData=cur.fetchone()
		print(f"dbdata={dbData}")
		if(dbData is not None): 
			dt,bucketName,filePath,qc,isTranscoded,fn= dbData
		else:
			db.close()
			print(f"{self.getTime()} - Nothing to Do")
			return(False)
		db.close()
		cur,db=dbconn()
		cur.execute(f"update s3transcoder set isTranscoded='10%' where filename='{fn}';")
		db.commit()
		db.close()
		basefn=fn.split('.')[0].replace(' ','_')
		basefn=re.sub(r"[\(\)]",'',basefn)
		fps,codec_name=self.getMeta(fn)
		gop=str(int(fps)*2)
		input_opts=" -async 1 -vsync 1 "
		f=open(f'{scriptdir}/logs/{basefn}.log','w+')
		f.close()
		#cmd=f"FFREPORT=file={scriptdir}/logs/{basefn}.log:level=32 ffmpeg -y {input_opts} -i \"{download_dir}/{fn}\"  "
		cmd=f"ffmpeg -y {input_opts} -i \"{download_dir}/{fn}\"  "
		ttl_flavors=len(transcode_profile)
		ttl_flavors+=1
		filter_opts=" -filter_complex \"[0:v]format=nv12,split=%s" % (ttl_flavors)
		count=1
		filter_scale_opts=""
		split_opts=""
		transcode_opts=""
		mp4Files=[]
		for flavor in transcode_profile:
			split_opts+="[s_v%s]" % (count)
			vbitrate=flavor.split('|')[0]
			res=flavor.split('|')[1]
			abitrate=flavor.split('|')[2]
			vcrop=flavor.split('|')[3]
			mrate=int(vbitrate)*10
			if(vcrop == '0'):
				filter_scale_opts+="[s_v%s]scale=%s,format=yuv420p[out%s];" % (count,res,count)
			else:
				filter_scale_opts+="[s_v%s]scale=%s:force_original_aspect_ratio=increase,crop=%s[out%s];" % (count,res,res,count)
			op_fn="%s/mp4/%s_%s.mp4" % (output_dir,basefn,vbitrate)
			mp4Files.append(op_fn)
			transcode_opts+=" -map \"[out%s]\" -c:v libx264 -r:v %s -g:v %s -b:v %s -maxrate %s -preset:v ultrafast -metadata service_provider=multitv -metadata service_name=multitv -map 0:a -c:a aac -b:a %s -ar 48000 %s " % (count,fps,gop,vbitrate,mrate,abitrate,op_fn)
			count+=1
		filter_scale_opts=filter_scale_opts[:-1]
		filter_opts+=" %s;%s\"" % (split_opts,filter_scale_opts)
		cmd+=filter_opts
		cmd+=transcode_opts
		fileSize=str(round(int(os.path.getsize("%s/%s" % (download_dir,fn)))/1024/1024))
		print(f"{self.getTime()} - Starting transcoding {fn}, FileSize={fileSize}MB")
		print(cmd)
		run(shlex.split(cmd))
		"""p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		if(p.returncode != 0):
			status="FF-Failed"
		else:
			status="Ok" """
		status="Ok"
		print(f"{self.getTime()} - Transcoding completed, Status={status}")
		cur,db=dbconn()
		cur.execute(f"update s3transcoder set isTranscoded='40%' where filename='{fn}';")
		db.commit()
		db.close()
		packager_cmd="/usr/bin/packager "
		lowResPackagerCmd="/usr/bin/packager "
		try:
			os.makedirs("%s/hls/%s" % (output_dir,basefn))
		except:
			pass
		playlists=['master.m3u8','eng.m3u8','lowres.m3u8','lowres_eng.m3u8']
		count=1
		for mp4fn in mp4Files:
			vbitrate=mp4fn.split('.')[0].split('_')[-1]
			playlists.append(f"{vbitrate}.m3u8")
			if(count == 1):
				lowResPackagerCmd+="'in=%s,stream=video,segment_template=%s/hls/%s/%s_lowres_$Number$.ts,playlist_name=%s_lowres.m3u8' " % (mp4fn,output_dir,basefn,vbitrate,vbitrate)
			packager_cmd+="'in=%s,stream=video,segment_template=%s/hls/%s/%s_$Number$.ts,playlist_name=%s.m3u8' " % (mp4fn,output_dir,basefn,vbitrate,vbitrate)
			count+=1
		packager_cmd+="'in=%s,stream=1,segment_template=%s/hls/%s/$Number$.aac,language=eng,hls_name=eng,playlist_name=eng.m3u8' " % (mp4fn,output_dir,basefn)
		lowResPackagerCmd+="'in=%s,stream=1,segment_template=%s/hls/%s/lowres_$Number$.aac,language=eng,hls_name=eng,playlist_name=lowres_eng.m3u8' " % (mp4fn,output_dir,basefn)
		packager_cmd+=" --segment_duration 4 --hls_master_playlist_output %s/hls/%s/master.m3u8 " % (output_dir,basefn)
		lowResPackagerCmd+=" --segment_duration 4 --hls_master_playlist_output %s/hls/%s/lowres.m3u8 " % (output_dir,basefn)
		#print(packager_cmd)
		print(f"{self.getTime()} - Starting Packaging")
		p=Popen(packager_cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		if(p.returncode != 0):
			status="P-Failed"
		else:
			status="Ok"
		print(f"{self.getTime()} - Starting LowRes")
		p=Popen(lowResPackagerCmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		#p=Popen(lowResPackagerCmd,stdout=PIPE,stderr=PIPE,shell=True)
		#out,err=p.communicate()
		print(f"{self.getTime()} - Packaging completed, Status={status}")
		cur,db=dbconn()
		if(status == 'Ok'):
			cur.execute(f"update s3transcoder set isTranscoded='70%' where filename='{fn}';")
		else:
			cur.execute(f"update s3transcoder set isTranscoded='{status}' where filename='{fn}';")
		db.commit()
		db.close()
		for playlist in playlists:
			self.sortPlaylist("%s/hls/%s/%s" % (output_dir,basefn,playlist))
		#self.sortPlaylist("%s/hls/%s/master.m3u8" % (output_dir,basefn))
		self.genThumb(output_dir,basefn,mp4fn)
		cur,db=dbconn()
		cur.execute(f"update s3transcoder set isTranscoded='{status}' where filename='{fn}';")
		db.commit()
		db.close()
		uploadDir="%s/hls/%s" % (output_dir,basefn)
		upload_hls=self.upload(uploadDir,basefn,fn)
		cur,db=dbconn()
		now = datetime.now()
		dt = now.strftime("%Y/%m/%d %H:%M:%S")
		if(upload_hls is True):
			cur,db=dbconn()
			cur.execute(f"update s3transcoder set isUploaded='Ok',completition_time='{dt}' where filename='{fn}';")
			print(f"{self.getTime()} - Uploaded")
		else:
			cur.execute(f"update s3transcoder set isUploaded='Failed' where filename='{fn}';")
			print(f"{self.getTime()} - Upload Failed")
		db.commit()
		db.close()
		return(status)

s=transcode()
downloadFile=s.getFile()
if(downloadFile is not False):	s.qc(downloadFile)
#if(downloadFile is not False):	s.transcoder()
s.transcoder()
"""while True:
	try:
		s=transcode()
		downloadFile=s.getFile()
		if(downloadFile is True):	s.qc(downloadFile)
		print 'False' if(downloadFile is not False):	s.transcoder()
		sleep(10)
	except KeyboardInterrupt:
		sys.exit()
	except Exception as e:
		print(e)
		continue"""
