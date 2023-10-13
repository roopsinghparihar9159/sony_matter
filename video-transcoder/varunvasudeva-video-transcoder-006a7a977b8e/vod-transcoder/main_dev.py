from email.mime import base

from requests import request,post
from dbconn import *
from conf import *
import os, sys
import boto3
from subprocess import PIPE, Popen
from datetime import datetime
from time import sleep
import json
import m3u8
import re
import random
import ast
from sys import argv
import shutil
import urllib.parse
import DownloadProgressBar
import logging
import iso639



class transcode(object):
	def __init__(self):
		self.logfile=transcode_log
		if(os.path.exists(f"{self.logfile}") is True):
			os.makedirs(f"{self.logfile}")
		logging.basicConfig(filename="logs/transcode.log", format='%(asctime)s %(message)s',filemode='w')
		self.logger = logging.getLogger()
		self.logger.setLevel(logging.DEBUG)
   
	def getTime(self):
		now = datetime.now()
		date=now.strftime("%Y-%m-%d %H:%M:%S")
		return(date)

	def removejsonchar(self,data):
		data=data[:-2]
		data=data[1:]
		return(data)

	def getFile(self,srturl):
		if('+' in srturl):
			video_file_path=srturl.replace('+',' ')
		if(' ' in srturl):
			video_file_path=urllib.parse.quote(srturl)
		else:
			video_file_path=srturl
		video_file_path=video_file_path.replace(' ','%20')
		video_file_name=video_file_path.split('/')[-1]
		print(f"{self.getTime()} - Downloading {video_file_path}")
		downloadFn=f"{download_dir}/{video_file_name}"
		self.logger.debug(f"Downloading {video_file_path} as {downloadFn}")
		try:
			DownloadProgressBar.download_url(video_file_path,downloadFn)
		except:
			pass
		if(os.path.exists(downloadFn) is True):
			self.logger.debug(f"Download {downloadFn} successful")
			return(video_file_name)
		else:
			self.logger.debug(f"Download failed {downloadFn}")
			return('False')

	def genThumb(self,output_dir,basefn,fn):
		cmd="ffmpeg -y -i '%s' -f image2 -vframes 1 %s/hls/%s/master.png" % (fn,output_dir,basefn)
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		if(p.returncode != 0):
			print(f"{self.getTime()} - Thumbnail Generation Failed")
			return(False)
		else:
			print(f"{self.getTime()} - Thumbnail Generated")
			return(True)

	def postTranscodingStatus(self,content_id,status,baseUrl):
		url=f"https://{baseUrl}/crons/transcodeupdate"
		body=body ={'content_id': content_id,'status':status}
		print(body)
		r=post(url,json=body)
		print(r.text)
		return(True)

	def postEncodeStatus(self,content_id,duration,cfurl,baseUrl):
		url=f"https://{baseUrl}/crons/tanscoded_url"
		body ={'content_id': content_id,'duration':duration,'abr':cfurl}
		print(body)
		r=post(url,json=body)
		print(r.text)
		return(True)
  
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

	def upload(self,bucketName,uploadFn,baseFn,fn,otype='HLS'):
		s3 = boto3.client('s3')
		"""cur,db=dbconn()
		cur.execute(f"select bucketname from s3transcoder where filename='{fn}'")
		bucketName=cur.fetchone()[0]"""
		cmd="/usr/local/bin/aws s3 cp %s s3://%s/multitv/output/%s/%s/ --recursive" % (uploadFn,bucketName,otype,baseFn)
		print(cmd)
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		err=err.decode('utf-8')
		if(err != ''):
			return(False)
		else:
			return(True)

	def getMeta(self,fn):
		cmd="ffprobe -v quiet -show_streams -print_format json \"%s/%s\"" % (download_dir,fn)
		print(cmd)
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

	def transcoder(self,hwdev):
		status='Ok'
		interlace_opts=''
		cur,db=dbconn()
		cur.execute("select app_id,content_id,path,filename,gpu_compatible from LOC_transcoder where isTranscoded='0' and qc='Ok' and app_id='911' limit 0,1;")
		#cur.execute("select app_id,content_id,path,filename,gpu_compatible from LOC_transcoder where isTranscoded='0' and qc='Ok' and app_id='911' limit 0,1;")
		dbData=cur.fetchone()
		if(dbData is not None): 
			app_id,content_id,path,fn,gpu_compatible= dbData
		else:
			db.close()
			print(f"{self.getTime()} - Nothing to Do")
			return(False)
		db.close()
		cur,db=dbconn()
		cur.execute(f"update LOC_transcoder set isTranscoded='-1' where filename='{fn}' and app_id='{app_id}' and content_id='{content_id}';")
		db.commit()
		db.close()
		f=open(path,'r')
		data=f.read()
		f.close()
		#data=ast.literal_eval(self.removejsonchar(data))
		data=ast.literal_eval(data)
		#print(data)
		data=data['content_id']
		basefn=fn.split('.')[0].replace(' ','_')
		basefn=re.sub(r"[\(\)]",'',basefn)
		video_file_path=f"{output_dir}/src"
		fps,codec_name,duration=self.getMeta(f"{fn}")
		print(fps,codec_name,duration)
		gop=float(fps)*2
		gop="%.2f" % gop
		interlace_opts="-deint 2 -drop_second_field 0"
		if(gpu_compatible==1):
			if(codec_name == 'h264'):
				input_opts=" -hwaccel_device %s -hwaccel cuvid -c:v h264_cuvid " % (hwdev)
				cudaDownloadOpts="hwdownload,"
			elif(codec_name == 'mpeg2video'):
				input_opts=" -hwaccel_device %s -hwaccel cuvid -c:v mpeg2_cuvid " % (hwdev)
				cudaDownloadOpts="hwdownload,"
		else:
			input_opts=""
			cudaDownloadOpts=""
		#print(input_opts)
		cmd="FFREPORT=file=logs/%s.log:level=32 ffmpeg -y %s %s -async 1 -vsync 1 -i '%s/%s'  " % (basefn,input_opts,interlace_opts,download_dir,fn)
		#ttl_flavors=len(transcode_profile)
		ttl_flavors=len(data)
		#return(True)
		#filter_opts=" -filter_complex \"[0:v]%sformat=nv12,yadif=mode=1,split=%s" % (cudaDownloadOpts,ttl_flavors)
		count=1
		filter_scale_opts=""
		split_opts=""
		transcode_opts=""
		mp4Files=[]
		check_DRM = data[0]['is_drm']
		for flavor in data:
			print(flavor)
			split_opts+="[s_v%s]" % (count)
			vbitrate=flavor['vb'].replace('k','000')
			width,height=flavor['screen'].split('x')
			abitrate=flavor['ab']
			baseUrl=flavor['base_url']
			mrate=int(vbitrate)*10
			if(mrate > 10000000): mrate="16000000"
			bucket=flavor["bucket"]
			content_id=flavor['content_id']
			cfUrl=flavor['cloudfront']
			#filter_scale_opts+="[s_v%s]scale=%s,format=yuv420p,hwupload_cuda[out%s];" % (count,res,count)
			if(gpu_compatible==1):
				scale_opts="-vf scale_cuda=w=%s:h=%s" % (width,height)
			else:
				scale_opts="-s %sx%s -pix_fmt yuv420p" % (width,height)
			op_fn="%s/mp4/%s_%s.mp4" % (output_dir,basefn,vbitrate)
			mp4Files.append(op_fn)
			transcode_opts+=" -map \"0:v\" -c:v h264_nvenc -r:v %s -g:v %s -b:v %s -maxrate %s -qmax:v 22.0 -preset:v slow -rc:v vbr -rc-lookahead:v 32 %s -no-scenecut 1 -metadata service_provider=multitv -metadata service_name=multitv -map 0:a -c:a aac -b:a %s -ar 48000 %s " % (fps,gop,vbitrate,mrate,scale_opts,abitrate,op_fn)
			count+=1
			if check_DRM == '1':
				access_key = flavor['access_key']
				drm_cid = flavor['drm_cid']
				site_id = flavor['site_id']
			elif check_DRM == '0':
				print("Non DRM")
			try:
				subtitlesData=flavor['subtitle']
			except:
				subtitlesData=None
			#"access_key":"rlUiNnyG5MvbcYAULKwf13jAPyrzlCBg","drm_cid":"105845","site_id":"JKJG"
		#transcode_opts+=" -map \"0:v\" -c:v h264_nvenc -r:v %s -g:v %s -b:v 15M -maxrate 15M -qmax:v 22.0 -preset:v slow -rc:v vbr -rc-lookahead:v 32 -no-scenecut 1 -metadata service_provider=multitv -metadata service_name=multitv -map 0:a -c:a aac -b:a %s -ar 48000 <output> " % (fps,gop,abitrate)
		print(transcode_opts)
		cmd+=transcode_opts
		fileSize=str(round(int(os.path.getsize("%s/%s" % (download_dir,fn)))/1024/1024))
		print(f"{self.getTime()} - Starting transcoding {fn}, FileSize={fileSize}MB")
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		if(p.returncode != 0): status="FF-Failed"
		else: status="Ok"
		"""cur,db=dbconn()	#Uncomment while moving to production
		cur.execute(f"update LOC_transcoder set isTranscoded='{status}',percentage='50%' where filename='{fn}' and app_id='{app_id}' and content_id='{content_id}';")
		db.commit()
		db.close()"""
		if(p.returncode != 0):
			status="Transcoding-Failed"
			self.postTranscodingStatus(content_id,status)
			return(status)
		print(f"{self.getTime()} - Transcoding completed, Status={status}")
		subsInput=""
		
		if check_DRM == '1':
			if(subtitlesData != None):
			#Subtitle convert###################################################
				for subs in subtitlesData:
					srtFilePath=subs['srt']
					srtLang=iso639.find(subs['lang'])['iso639_2_b']
					print(srtFilePath,srtLang)
					srtFileName=self.getFile(srtFilePath)
					cmd=f"srt-vtt -o {download_dir}/ {download_dir}/{srtFileName}"
					p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
					out,err=p.communicate()
					srtFileName=srtFileName.replace('srt','vtt')
					subsInput+=f"{download_dir}/{srtFileName}:name={subs['lang']}:lang={srtLang} "
					print(subsInput)
			#####################################################################
			print('DRM_started')
			drm_input = ""
			for mp4fn in mp4Files: drm_input += f"{mp4fn} "
			#drm_PACKAGER = f"PallyConPackager -f --site_id {site_id} --access_key {access_key} --content_id {content_id} --dash --hls -i {drm_input} -o {content_id}" #! NEED TO CHECK OUTPUT DIRECTORY
			drm_PACKAGER = f"PallyConPackager -f --skip_pallycon_custom_info --ascending_track_order_in_manifest --site_id {site_id} --access_key {access_key} --content_id {content_id} --dash --hls -i {drm_input} --fragment_duration 4 --mpd_filename master.mpd --subtitle {subsInput} -o /tmp/{basefn}"
			print(drm_PACKAGER)
			print(f"{self.getTime()} - Starting Packaging")
			p = Popen(drm_PACKAGER,stdout=PIPE,stderr=PIPE,shell=True)
			out,err = p.communicate()
			destination=f"{output_dir}/hls/{basefn}/"
			if(os.path.exists(destination) == True):
				src=f"/tmp/{basefn}/dash/*"
			else:
				src=f"/tmp/{basefn}/dash"
			#shutil.move(src,destination,dirs_exist_ok=False)
			cp_cmd=f"cp -rvf {src} {destination}"
			print(cp_cmd)
			p=Popen(cp_cmd,stdout=PIPE,stderr=PIPE,shell=True)
			out,err=p.communicate()
			#print(out,err)
			status = "P-Failed" if(p.returncode != 0) else "Ok"
			cfUrl=f"{cfUrl}/multitv/output/HLS/{basefn}/master.mpd"
			#output_url_dash = f"{data[0]['cloudfront']}/{data[0]['bucket']}/{content_id}/dash/stream.mpd" # need to cross check
			#output_url_hls = f"{data[0]['cloudfront']}/{data[0]['bucket']}/{content_id}/hls/master.m3u8"  # need to cross check
		elif check_DRM == '0':
			print('Non DRM Started')
			if(subtitlesData != None):
				for subs in subtitlesData:
					srtFilePath=subs['srt']
					srtLang=iso639.find(subs['lang'])['iso639_2_b']
					print(srtFilePath,srtLang)
					srtFileName=self.getFile(srtFilePath)
					cmd=f"srt-vtt -o {download_dir}/ {download_dir}/{srtFileName}"
					p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
					out,err=p.communicate()
					srtFileName=srtFileName.replace('srt','vtt')
					#subsInput+=f"{download_dir}/{srtFileName}:name={subs['lang']}:lang={srtLang} "
					subsInput+=f"'in={download_dir}/{srtFileName},stream=text,segment_template={output_dir}/{basefn}/{srtLang}_$Number$.vtt,playlist_name={output_dir}/{basefn}/{srtLang}_main.m3u8,hls_group_id=text,hls_name={subs['lang']}' "
				print(subsInput)
			packager_cmd="/usr/bin/packager "
			try:
				os.makedirs("%s/hls/%s" % (output_dir,basefn))
			except:
				pass
			playlists=['master.m3u8','eng.m3u8']
			for mp4fn in mp4Files:
				vbitrate=mp4fn.split('.')[0].split('_')[-1]
				playlists.append(f"{vbitrate}.m3u8")
				packager_cmd+=" 'in=%s,stream=video,segment_template=%s/hls/%s/%s_$Number$.ts,playlist_name=%s.m3u8' " % (mp4fn,output_dir,basefn,vbitrate,vbitrate)
			packager_cmd+=" 'in=%s,stream=1,segment_template=%s/hls/%s/$Number$.aac,language=eng,hls_name=eng,playlist_name=eng.m3u8' " % (mp4fn,output_dir,basefn)
			packager_cmd+=f" {subsInput} "
			packager_cmd+=" --segment_duration 4 --hls_master_playlist_output %s/hls/%s/master.m3u8 " % (output_dir,basefn)
			print(packager_cmd)
			print(f"{self.getTime()} - Starting Packaging")
			p=Popen(packager_cmd,stdout=PIPE,stderr=PIPE,shell=True)
			out,err=p.communicate()
			if(p.returncode != 0):
				status = "P-Failed"
			else:
				status = "Ok"
			##DASH Creation##
			packager_cmd = "/usr/bin/packager " 
			try:
				os.makedirs("%s/hls/%s" % (output_dir,basefn))
				os.makedirs("%s/dash/%s" % (output_dir,basefn))
			except:
				pass
			playlists=['master.m3u8','eng.m3u8']
			for mp4fn in mp4Files:
				vbitrate = mp4fn.split('.')[0].split('_')[-1]
				playlists.append(f"{vbitrate}.m3u8")
				#packager_cmd+="'in=%s,stream=video,init_segment=h264_%s/init.mp4,segment_template=%s/dash/%s/%s_$Number$.m4s,playlist_name=%s.m3u8' " % (mp4fn,vbitrate,output_dir,basefn,vbitrate,vbitrate)
				packager_cmd += f"'in={mp4fn},stream=video,init_segment={output_dir}/dash/{basefn}/init_{vbitrate}.mp4,segment_template={output_dir}/dash/{basefn}/{vbitrate}_$Number$.m4s,playlist_name={vbitrate}.m3u8' "
			packager_cmd += f"'in={mp4fn},stream=1,init_segment={output_dir}/dash/{basefn}/aud_init.mp4,segment_template=output_dir/dash/basefn/$Number$.m4s,language=eng,hls_name=eng,playlist_name=eng.m4s' "
			packager_cmd += f" --segment_duration 4 --mpd_output {output_dir}/dash/{basefn}/master.mpd "
			#print(packager_cmd) 
			print(f"{self.getTime()} - Starting Packaging")
			for playlist in playlists:
				self.sortPlaylist("%s/hls/%s/%s" % (output_dir,basefn,playlist))
			cfUrl=f"{cfUrl}/multitv/output/HLS/{basefn}/master.m3u8"
		print(f"{self.getTime()} - Packaging completed, Status={status}")
		cur,db = dbconn()
		cur.execute(f"update LOC_transcoder set isTranscoded='{status}',percentage='75%' where filename='{fn}' and app_id='{app_id}' and content_id='{content_id}';")
		db.commit()
		db.close()
		if(p.returncode != 0):
			status = "Packaging-Failed"
			self.postTranscodingStatus(content_id,status,baseUrl)
			return(status)
		#self.sortPlaylist("%s/hls/%s/master.m3u8" % (output_dir,basefn))
		self.genThumb(output_dir,basefn,mp4fn)
		uploadDir = "%s/hls/%s" % (output_dir,basefn)
		upload_hls = self.upload(bucket,uploadDir,basefn,fn)
		if(upload_hls is True):
			status='Ok'
			print(f"{self.getTime()} - Uploaded")
		else:
			status='Failed'
			print(f"{self.getTime()} - Upload Failed")
		cur,db = dbconn()
		cur.execute(f"update LOC_transcoder set isUploaded='{status}',percentage='99%' where filename='{fn}' and app_id='{app_id}' and content_id='{content_id}';")
		db.commit()
		db.close()
		self.postEncodeStatus(content_id,duration,cfUrl,baseUrl)
		status="completed"
		self.postTranscodingStatus(content_id,status,baseUrl)
		return(status)
hwdev=argv[1]
"""s=transcode()
s.transcoder(hwdev)"""

while True:
	try:
		s=transcode()
		s.transcoder(hwdev)
		sleep(random.randint(2, 20))
	except KeyboardInterrupt:
		sys.exit()
	except Exception as e:
		print(e)
		continue