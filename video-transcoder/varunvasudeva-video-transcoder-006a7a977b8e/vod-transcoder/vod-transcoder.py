from requests import post, get
from dbconn import *
from conf import *
import os, boto3, json, m3u8, urllib.parse, DownloadProgressBar, logging, iso639, re,  string, random, uuid, xmltodict, base64 #ast, glob,
from subprocess import PIPE, Popen
from datetime import datetime, timedelta
from sys import argv # from akamai.netstorage import Netstorage #, NetstorageError # from time import sleep


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
		date = now.strftime("%Y-%m-%d %H:%M:%S")
		return(date)

	def removejsonchar(self,data):
		data = data[:-2]
		data = data[1:]
		return(data)

	#'subtitle': [{'srt': 'https://sftp1.multitvsolution.com/FTP/1061/multitv/MT.srt', 'lang': 'English'}, {'srt': 'https://sftp1.multitvsolution.com/FTP/1061/multitv/MT.srt', 'lang': 'Hindi'}, {'srt': 'https://sftp1.multitvsolution.com/FTP/1061/multitv/MT.srt', 'lang': 'Urdu'}]
	def getFile(self,srturl,srt_fileLANG):
		if('+' in srturl):
			video_file_path = srturl.replace('+',' ')
		if(' ' in srturl):
			video_file_path = urllib.parse.quote(srturl)
		else:
			video_file_path = srturl
		video_file_path = video_file_path.replace('%3A',':')
		video_file_path = video_file_path.replace(' ','%20')
		video_file_name = video_file_path.split('/')[-1]
		video_file_name = video_file_name.replace(".srt",f"_{srt_fileLANG}.srt") if ".srt" in video_file_name else (video_file_name.replace(".SRT", f"_{srt_fileLANG}.srt") if ".SRT" in video_file_name else (video_file_name.replace(".vtt",f"_{srt_fileLANG}.vtt") if ".vtt" in video_file_name else ""))
		print(f"{self.getTime()} - Downloading {video_file_path}")
		downloadFn = f"{download_dir}/{video_file_name}"
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

	def genThumb(self,output_dir,basefn,fn,duration):
		ori_sz = os.popen(f"ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 {fn}").read().strip("\n")
		# print(a,type(a))
		squar_sz = ori_sz.split("x")[1] #print(squar_sz)
		size_16 = int(squar_sz)//9
		size_16 = int(squar_sz)-size_16
		size_9 = int((size_16*9)/16)
		TM_dur = []
		TM_dur.append(str(timedelta(seconds=int(int(float(duration))/4))))
		os.system(f"ffmpeg -y -i '{fn}' -f image2  -ss {TM_dur[0]} -s {ori_sz} -compression_level 100 -vframes 1 {output_dir}/output/{basefn}/master.png")
		os.system(f"ffmpeg -y -i '{output_dir}/output/{basefn}/master.png' -vf 'crop={size_9}:{size_16}' {output_dir}/output/{basefn}/master9-16.png")
		os.system(f"ffmpeg -y -i '{output_dir}/output/{basefn}/master.png' -vf 'crop={squar_sz}:{squar_sz}' {output_dir}/output/{basefn}/mastersqaure.png")
		# percn = [25,50,75] # TM_dur = [] # TM_dur.append(str(timedelta(seconds=int(int(float(duration))/4)))) # TM_dur.append(str(timedelta(seconds=int(int(float(duration))/2)))) # TM_dur.append(str(timedelta(seconds=int((int(float(duration))*3)/4)))) # for i in range(len(TM_dur)): # 	video = mp.VideoFileClip(fn) # 	video.save_frame(f"{output_dir}/hls/{basefn}/master_{percn[i]}.png",t=TM_dur[i]) # cmd = f"ffmpeg -y -i '{fn}' -f image2 -ss {TM_dur[i]} -vframes 1 {output_dir}/hls/{basefn}/master_{percn[i]}.png" # p = Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True) # out,err = p.communicate() # print(out,err) #todo

	def genGIF(self,fnn,outFN,duration):
		# timee = int(duration/4) #277 seconds  277/4 = 69seconds  00:01:09
		strt_tm = str(timedelta(seconds=int(int(float(duration))/4)))
    	#todo for GIF
		cmd_GIF = f"ffmpeg -ss {strt_tm} -t 5 -y -i {fnn} -vf 'scale=iw/6:ih/6' -f gif {outFN}"
		print("GIFF: ",cmd_GIF)
		os.system(cmd_GIF) # pp = Popen(cmd_GIF,stdout=PIPE,stderr=PIPE,shell=True) # out,err = pp.communicate() # print("LINE 89: ",out,err)
		print(f"{self.getTime()} - GIF completed")
		#todo##########

	def postTranscodingStatus(self,content_id,status,baseUrl,error_code):
		url = f"https://{baseUrl}/crons/transcodeupdate"
		body = {'content_id': content_id,'status':status,'error_code':error_code}
		r = post(url,json=body)
		print(r.text)
		return(True)

	def postEncodeStatusBothnonandnonDRM(self,content_id,duration,mpdcfUrl,m3u8cfUrl,baseUrl,gifurl,thumbURL,keyid):
		url=f"https://{baseUrl}/crons/tanscoded_url"
		body = {'content_id': content_id,'duration':duration,'abr':m3u8cfUrl,'abr_drm':mpdcfUrl,'gif':gifurl,'thumb':thumbURL,'k_id':keyid}
		print(body)
		r=post(url,json=body)
		print(r.text)
		return(True)

	# def postEncodeStatus(self,content_id,duration,cfurl,baseUrl,gifurl,thumbURL): # 	url=f"https://{baseUrl}/crons/tanscoded_url" # 	body = {'content_id': content_id,'duration':duration,'abr':cfurl,'gif':gifurl,'thumb':thumbURL}  # 	r=post(url,json=body) # 	print(r.text) # 	return(True)
	
	def getDrmKey(self, content_id):
		EZusername="siddharth.s@multitvsolution.com"
		EZpassword="s3cur3R4nKuMMpK1ck"
		kid=uuid.uuid4()
		url = f"https://cpix.ezdrm.com/keygenerator/cpix2.aspx?k={kid}&u={EZusername}&p={EZpassword}&c={content_id}"
		self.telUpdater(content_id,url)
		r=get(url)
		try:
			response = r.text
			print(r.text)
			data = xmltodict.parse(response)
			keyy = data['cpix:CPIX']['cpix:ContentKeyList']['cpix:ContentKey']['cpix:Data']['pskc:Secret']['pskc:PlainValue']
			keyy = base64.b64decode(keyy).hex()
			print(kid,keyy)
			return (str(kid).replace("-",""),keyy)
		except:
			print("keyerror")
			self.telUpdater(content_id,url)
			return ("keyerror","keyerror")

	def sortPlaylist(self,masterfn):
		srcf = open(masterfn,'r')
		playlist_text = srcf.read()
		srcf.close()
		parsed_playlist = m3u8.loads(playlist_text)
		parsed_playlist.playlists.sort(key=lambda x: x.stream_info.average_bandwidth)
		new_playlist_text = parsed_playlist.dumps()       
		f=open(masterfn,'w+')
		f.write(new_playlist_text)
		f.close()
		return(True)

	def upload(self,bucketName,uploadFn,baseFn,fn,otype='output'):
		s3 = boto3.client('s3')
		"""cur,db=dbconn()
		cur.execute(f"select bucketname from s3transcoder where filename='{fn}'")
		bucketName=cur.fetchone()[0]"""
		cmd = "/usr/local/bin/aws s3 cp %s s3://%s/multitv/%s/%s/ --recursive" % (uploadFn,bucketName,otype,baseFn)
		print(cmd)
		p = Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err = p.communicate()
		err = err.decode('utf-8')
		if(err != ''):
			return(False)
		else:
			return(True)

	def upload_netstorage(self,bucketName,uploaddir,baseFn,fn,NS_CPCODE,NS_KEY,NS_KEYNAME,NS_HOSTNAME):
		print("uploading to netstorage")
		#todo rsync -arz --progress --password-file=/home/transcoder/.secrets /storage/data/output/1061_6470a50347da0/ universal-mtv@alt.rsync.upload.akamai.com::universal-mtv/1436641/multitv/output/1061_6470a50347da0/
		os.system(f"rsync -arz --progress --password-file=/home/transcoder/.secrets {uploaddir} universal-mtv@alt.rsync.upload.akamai.com::universal-mtv/{NS_CPCODE}/{bucketName}/output/")
		# ns = Netstorage(NS_HOSTNAME, NS_KEYNAME, NS_KEY, ssl=False) # for filename in glob.iglob(uploaddir+"/**", recursive=True): # 	# print(filename if "." in filename else None) # 		local_source = filename if "." in filename else None # 		if local_source != None: # 			destination_FN = local_source.replace("/storage/data/","") # 			netstorage_destination = f"/{NS_CPCODE}/{bucketName}/{destination_FN}" # 			print("LOCAL SOURCE: ",local_source," DESTINATION: ",netstorage_destination) # 			ok, response = ns.upload(local_source, netstorage_destination) # 			print( ok, " -- ",response) # print( ok, " -- ",response) # if(ok == True): return(True) # else: return(False)
		return True
    	## https://altbalaji-new.multitvsolution.com/onedrive/61c87ef695cb7.mp4 #  https://altbalaji-new.multitvsolution.com/multitv/hls/1099_641a97389ea15/mastersqaure.png
    
	def timetosec(self,timestring):
		timestring = timestring.split('.')[0]
		pt = datetime.strptime(timestring,'%H:%M:%S')
		total_seconds = pt.second + pt.minute*60 + pt.hour*3600
    	# print(type(total_seconds))
		return str(total_seconds)

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
					duration = data['tags']['DURATION'] if fn.endswith(".webm") else data['duration']
					duration = self.timetosec(duration) if fn.endswith(".webm") else duration
				except:
					duration='0'
				return(fps,codec_name,duration)
			elif (data['codec_type'] == 'audio'):
				fps=0 #as there is no fps in audio
				codec_name="MP3" #data['codec_name']
				duration=data['duration']
		# print(fps,codec_name,duration)
				return(fps,codec_name,duration)

	def DB_updater(self,content_id,app_id,file_name,typee,value,percentage):
		payload={'content_id': content_id,'app_id': app_id,'file_name': file_name,'typee': typee,'value': value,'percentage': percentage}
		response = post(db_update_API, data=payload)
		print(response,response.text)
		return response.text

	def tmUpdater(self,content_id):
		response = get(complete_tmAPI%content_id)
		print(response,response.text)
		return response.text

	def telUpdater(self,content_id,status):
		
		print("telUpdater")
	
	def logWriter(self, file_loc,content_id,status):
		f = open(file_loc, "a+" )
		f.write(f'{content_id} {status} @ {self.getTime()}\n')
		f.close()
	
	def CHECK_vert(self,vid_url):
		res = os.popen(f"ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 {vid_url}").read().split("\n")[0]
		print(res)
		(a,b) = res.split("x")
		c= int(a) < int(b)
		return (c,res)

	def transcoder(self,hwdev):
		status='Ok'
		interlace_opts=''
		job_data = get(job_API%trans_details)
		# print(job_data,job_data.reason,job_data.text,type(job_data.text))
		if job_data.text == "No Data": 
			print(f"{self.getTime()} - Nothing to Do")
			return (False)
		else:
			js_data = json.loads(job_data.text)
			app_id,content_id,path,fn,gpu_compatible = js_data['dbdump'][0]['app_id'],js_data['dbdump'][0]["content_id"],js_data['dbdump'][0]["path"],js_data['dbdump'][0]["filename"],js_data['dbdump'][0]["gpu_compatible"]
		# cur,db=dbconn() # cur.execute("select app_id,content_id,path,filename,gpu_compatible from LOC_transcoder where isTranscoded='0' and qc='Ok' limit 0,1;") # #cur.execute("select app_id,content_id,path,filename,gpu_compatible from LOC_transcoder where isTranscoded='0' and qc='Ok' and app_id='911' limit 0,1;") # dbData=cur.fetchone() # if(dbData is not None):  # 	app_id,content_id,path,fn,gpu_compatible= dbData # else: # 	db.close() # 	print(f"{self.getTime()} - Nothing to Do") # 	return(False) # db.close()

		#todo#############
		self.DB_updater(content_id,app_id,fn,"transcoder","-1","10%")
		self.telUpdater(content_id,"Starts")
		
		# cur,db=dbconn() # cur.execute(f"update LOC_transcoder set isTranscoded='-1' where filename='{fn}' and app_id='{app_id}' and content_id='{content_id}';") # db.commit() # db.close()
		#todo#############
		#todo#############
		# f=open(path,'r') # data=f.read() # f.close() # #data = ast.literal_eval(self.removejsonchar(data)) # data=ast.literal_eval(data) #print(data)
		data = js_data['j_data']['content_id']
		#todo#############
		basefn=fn.split('.')[0].replace(' ','_')
		basefn=re.sub(r"[\(\)]",'',basefn)
		log_file = f"logs/{basefn}.txt"
		fileSize = str(round(int(os.path.getsize("%s/%s" % (download_dir,fn)))/1024/1024))
		fps,codec_name,duration=self.getMeta(f"{fn}")

		'''CODE for AUD transcoder STARTS'''
		#todo CODE for AUD transcoding...
		c_type = data[0]['c_type'] if 'c_type' in data[0] else ""
		if c_type == "audio":
			print("AUDIO only")
			pack_cmd_opts=""
			for flavor in data:
				ab=flavor['ab']
				file_url = flavor['video_file_name']
				outFilepath = flavor['name'].split(".")[0]
				outDr = f"{output_dir}/mp3/{outFilepath}"
				base_url = flavor['base_url']
				cf_url=flavor['cloudfront']
				try: os.makedirs(outDr)
				except: pass
				cur_bitrate = os.popen(f"ffprobe -v error -select_streams a:0 -show_entries stream=bit_rate -of default=noprint_wrappers=1:nokey=1 {file_url}").read().split("\n")[0]
				cur_bitrate = int(int(cur_bitrate)/1000)
				print("cur_bitrate",cur_bitrate)
				if cur_bitrate ==320: lis_ab = ['320','256']
				else: lis_ab= ['128','192']
				print("lis_ab",lis_ab)
			for i in lis_ab:
					
				cmd = f"ffmpeg -y -i '{file_url}' -c:a aac -ab {i}k {outDr}/{outFilepath}_{i}.m4a"
				p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
				out,err=p.communicate()
				#in=128_out.m4a,stream=audio,init_segment=128/init.mp4,segment_template=128_$Number$.m4s,playlist_name=128.m3u8,hls_name=128k
				pack_cmd_opts += f" 'in={outDr}/{outFilepath}_{i}.m4a,stream=audio,init_segment={outDr}/{i}/init.mp4,segment_template={outDr}/{i}_$Number$.m4s,playlist_name={i}.m3u8' "
			try: os.makedirs(f"{output_dir}/mp3/{outFilepath}")
			except: pass
			packager_cmd = f"/usr/bin/packager {pack_cmd_opts} --segment_duration 4 --hls_master_playlist_output {output_dir}/mp3/{outFilepath}/master.m3u8 "
			print(packager_cmd)
			print(f"{self.getTime()} - Starting Packaging")
			p = Popen(packager_cmd,stdout=PIPE,stderr=PIPE,shell=True)
			out,err = p.communicate()
			if(p.returncode != 0):
				status = "P-Failed"
				self.postTranscodingStatus(content_id,status,base_url,err.decode('utf-8'))
				self.DB_updater(content_id,app_id,fn,"transcoder","P-Fail","13%")
				return(status)
				# exit()
			else: status = "AUD"
			print("STATUS after PACKAGING: ",out,err)
			if status == "AUD":
				AOL_cpcode="1479023"
				AOL_bucket="multitv"
				uploadDir = f"{output_dir}/mp3/{outFilepath}"
				os.system(f"rsync -arz --progress --password-file=/home/transcoder/.secrets {uploadDir} universal-mtv@alt.rsync.upload.akamai.com::universal-mtv/{AOL_cpcode}/{AOL_bucket}/output/")
				# ns = Netstorage("art-of-living.ftp.upload.akamai.com", "art-of-living", "2HCG8OoWuay6AnKp8RZ9jjrM9zsuRJgj3aWiesitvLyBHKz4D", ssl=False)
				# for filename in glob.iglob(uploadDir+"/**", recursive=True):
				# 	local_source = filename if "." in filename else None
				# 	if local_source != None:
				# 		destination_FN = local_source.replace("/storage/data/","")
				# 		netstorage_destination = f"/{AOL_cpcode}/{AOL_bucket}/{destination_FN}"
				# 		print("LOCAL SOURCE: ",local_source," DESTINATION: ",netstorage_destination)
				# 		ok, response = ns.upload(local_source, netstorage_destination)
				# 		print( ok, " -- ",response)
				# print( ok, " -- ",response)
				final_url = f"{cf_url}/{AOL_bucket}/output/{outFilepath}/master.m3u8"
				self.DB_updater(content_id,app_id,fn,"transcoder",status,"75%")
				self.DB_updater(content_id,app_id,fn,"uploader",status,"100%")
				self.postEncodeStatusBothnonandnonDRM(content_id,'duration',final_url,final_url,base_url,final_url,final_url,'AUDIO')
			# if(ok == True): return(True) # else: return(False)
			return(status)
			exit()
		else: print("VIDEO continue")
		print("vid trans")
		#todo CODE for AUD transcoding...
		'''CODE for AUD transcoder ENDS'''
		#todo CODE for Vert  transcoding...
		check_vert,ress = self.CHECK_vert(f"{download_dir}/{fn}")
		if check_vert == True:
			#code for Vert Transcode...
			baseUrl=data[0]['base_url']
			cfUrl= data[0]['cloudfront']
			print("Verttt")
			flav = {"360x640":"64k","720x1280":"96k","1080x1920":"96k"} if ress == "1080x1920" else {"360x640":"64k","720x1280":"96k"}
			max_rate={"360x640":"5000000","720x1280":"16000000","1080x1920":"16000000"}
			bv = {"360x640":"500000","720x1280":"1350000","1080x1920":"3000000"}
			cmdd = f"ffmpeg -y  -async 1 -vsync 1 -i  '{download_dir}/{fn}' "
			flav_file=[]
			for keyy,vall in flav.items():
				op_fn=f"{output_dir}/mp4/{basefn}_{bv[keyy]}.mp4"
				flav_file.append(op_fn)
				cmdd += f"-map \"0:v\" -c:v libx264 -r:v 25.00 -g:v 50.00 -b:v {bv[keyy]} -maxrate {max_rate[keyy]} -preset:v fast -rc:v vbr  -s {keyy} -pix_fmt yuv420p -metadata service_provider=multitv -metadata service_name=multitv -map 0:a -c:a aac -b:a {vall} -ar 48000 {op_fn} "

			print("CMD: ",cmdd)
			self.telUpdater(content_id,f"VerTranscoding Starts FileSize={fileSize}MB")
			self.logWriter(log_file,content_id,f"VerTranscoding Starts FileSize={fileSize}MB")
			print(f"{self.getTime()} - Starting VerTranscoding {fn}, FileSize={fileSize}MB")
			p=Popen(cmdd,stdout=PIPE,stderr=PIPE,shell=True)
			out,err=p.communicate()
			if(p.returncode != 0):
				status = "Tr-Fail"
				self.postTranscodingStatus(content_id,"Transcoding-Failed",baseUrl,err.decode('utf-8'))#?'pending', 'inprocess', 'completed', 'error', 'download', 'spending', 'QC-Failed', 'Transcoding-Failed', 'Packaging-Failed'
				self.DB_updater(content_id,app_id,fn,"transcoder",status,"11%")
				self.tmUpdater(content_id)
				self.telUpdater(content_id,"Transcoding-Failed")
				self.telUpdater(content_id,err.decode('utf-8'))
				self.logWriter(log_file,content_id,f"Transcoding-Failed {cmd}")
				return(status)
			else: status='Ok'
		
			print(f"{self.getTime()} - Transcoding completed, Status={status}")
			self.telUpdater(content_id,"Transcoding Completed")
			self.logWriter(log_file,content_id,"Transcoding Completed")
			hls_ver_dir = f"{output_dir}/output/{basefn}/hls"
			packager_cmdv = "/usr/bin/packager "
			self.telUpdater(content_id,"Packaging Started")
			self.logWriter(log_file,content_id,"Packaging Started")
			for mp4fn in flav_file:
				vbitrate = mp4fn.split('.')[0].split('_')[-1]
				packager_cmdv += f" 'in={mp4fn},stream=video,segment_template={hls_ver_dir}/{vbitrate}_$Number$.ts,playlist_name={vbitrate}.m3u8' "
			try:
				default_lang = os.popen(f"ffprobe -v error -show_entries stream=index:stream_tags=language -select_streams a -of compact=p=0:nk=1 {download_dir}/{fn}").read().split("|")[1].strip() #todo must
				packager_cmdv += f" 'in={mp4fn},stream=1,segment_template={hls_ver_dir}/$Number$.aac,hls_name={default_lang},playlist_name={default_lang}.m3u8' "
				# playlists.append(f"{default_lang}.m3u8")
			except:
				print("No specific lang")
				default_lang = "hin"
				packager_cmdv += f" 'in={mp4fn},stream=1,segment_template={hls_ver_dir}/$Number$.aac,hls_name={default_lang},playlist_name={default_lang}.m3u8' "
				# playlists.append(f"{default_lang}.m3u8")
			master_hlsNAME = f"master_{''.join(random.choices(string.ascii_letters, k=16))}.m3u8"
			packager_cmdv += f" --segment_duration 4 --hls_master_playlist_output {hls_ver_dir}/{master_hlsNAME} "
			print(packager_cmdv)
			print(f"{self.getTime()} - Starting Packaging")
			p = Popen(packager_cmdv,stdout=PIPE,stderr=PIPE,shell=True)
			out,err = p.communicate()
			if(p.returncode != 0):
				status = "P-Fail"
				self.postTranscodingStatus(content_id,'Packaging-Failed',baseUrl,err.decode('utf-8'))
				self.DB_updater(content_id,app_id,fn,"transcoder",status,"12%")
				self.tmUpdater(content_id)
				self.telUpdater(content_id,"Packaging Failed")
				self.telUpdater(content_id,err.decode('utf-8'))
				self.logWriter(log_file,content_id,packager_cmd)
				return (status)
			else:
				status = "Ok"
			(f"{self.getTime()} - Completed Packaging: {status}")
			m3u8cfUrl= f"{cfUrl}/multitv/output/{basefn}/hls/{master_hlsNAME}"
			self.genThumb(output_dir,basefn,mp4fn,duration)
			self.telUpdater(content_id,"Packaging Completed")
			thumbURL=f"{cfUrl}/multitv/output/{basefn}/master.png"
			self.DB_updater(content_id,app_id,fn,"transcoder",status,"75%")
			uploadDir = "%s/output/%s" % (output_dir,basefn)
			os.system(f"rsync -arz --progress --password-file=/home/transcoder/.secrets {uploadDir} universal-mtv@alt.rsync.upload.akamai.com::universal-mtv/1436641/multitv/output/")
			self.DB_updater(content_id,app_id,fn,"uploader","ver","100%")
			self.postEncodeStatusBothnonandnonDRM(content_id,duration,m3u8cfUrl,m3u8cfUrl,baseUrl,m3u8cfUrl,thumbURL,"")
			return(status)
      	#todo CODE for Vert  transcoding...
		
		
		video_file_path=f"{output_dir}/src"
		# fps,codec_name,duration=self.getMeta(f"{fn}")
		print(fps,codec_name,duration)
		gop=float(fps)*2
		gop="%.2f" % gop
		interlace_opts="-deint 2 -drop_second_field 0"
		self.logWriter(log_file,content_id,"Starts")
		if(gpu_compatible==1):
			if(codec_name == 'h264'):
				input_opts=" -hwaccel_device %s -hwaccel cuvid -c:v h264_cuvid " % (hwdev)
				cudaDownloadOpts="hwdownload,"
			elif(codec_name == 'mpeg2video'):
				input_opts=" -hwaccel_device %s -hwaccel cuvid -c:v mpeg2_cuvid " % (hwdev)
				cudaDownloadOpts="hwdownload,"
			else: input_opts=""
		else:
			input_opts=""
			cudaDownloadOpts="" #print(input_opts)

		cmd="FFREPORT=file=logs/%s.log:level=32 ffmpeg -y %s %s -async 1 -vsync 1 -i '%s/%s'  " % (basefn,input_opts,interlace_opts,download_dir,fn) #ttl_flavors=len(transcode_profile)
		ttl_flavors=len(data) #return(True) #filter_opts=" -filter_complex \"[0:v]%sformat=nv12,yadif=mode=1,split=%s" % (cudaDownloadOpts,ttl_flavors)
		count=1
		filter_scale_opts=""
		split_opts=""
		transcode_opts=""
		mp4Files=[]
		check_DRM = data[0]['is_drm']
		drm_nonDRM = data[0]['drm_nondrm'] if 'drm_nondrm' in data[0] else ("1" if 'drm_nondrm' not in data[0] and check_DRM=="1" else "0" ) #todo
		upload_LOC = data[0]['upload_key'] if 'upload_key' in data[0] else "aws"

		for flavor in data:
			# print(flavor)
			split_opts+="[s_v%s]" % (count)
			vbitrate=flavor['vb'].replace('k','000')
			width,height=flavor['screen'].split('x')
			abitrate=flavor['ab']
			baseUrl=flavor['base_url']
			mrate=int(vbitrate)*10
			if(mrate > 10000000): mrate="16000000"
			bucket=flavor["bucket"]
			NS_CPCODE=flavor["cp_code"] if 'cp_code' in flavor else ""
			NS_KEY=flavor["netstorage_key"] if 'netstorage_key' in flavor else ""
			NS_KEYNAME=flavor["netstorage_keyName"] if 'netstorage_keyName' in flavor else ""
			NS_HOSTNAME=flavor["ns_host"] if 'ns_host' in flavor else ""
			content_id=flavor['content_id']
			cfUrl=flavor['cloudfront']
			httpcfurl=flavor['cloudfront'] #filter_scale_opts+="[s_v%s]scale=%s,format=yuv420p,hwupload_cuda[out%s];" % (count,res,count)
			if(gpu_compatible==1):
				scale_opts="-vf scale_cuda=w=%s:h=%s" % (width,height)
			else:
				scale_opts="-s %sx%s -pix_fmt yuv420p" % (width,height)
			op_fn="%s/mp4/%s_%s.mp4" % (output_dir,basefn,vbitrate)
			mp4Files.append(op_fn)
			transcode_opts+=" -map \"0:v\" -c:v h264_nvenc -r:v %s -g:v %s -b:v %s -maxrate %s  -preset:v fast -rc:v vbr  %s -metadata service_provider=multitv -metadata service_name=multitv -map 0:a -c:a aac -b:a %s -ar 48000 %s " % (fps,gop,vbitrate,mrate,scale_opts,abitrate,op_fn)
			count+=1
			access_key = flavor['access_key'] if 'access_key' in flavor else ""
			# drm_cid = flavor['drm_cid']
			site_id = flavor['site_id'] if 'site_id' in flavor else ""
			# if check_DRM == '1': # 	access_key = flavor['access_key'] # 	site_id = flavor['site_id'] # elif check_DRM == '0': print("Non DRM")
			try:
				subtitlesData = flavor['subtitle'] if flavor['subtitle'] != '' else None
			except: subtitlesData = None
			try:
				audioData = flavor['audio'] if flavor['audio'] != '' else None
			except: audioData = None
		cmd += transcode_opts
		# fileSize = str(round(int(os.path.getsize("%s/%s" % (download_dir,fn)))/1024/1024))
		print("CMD: ",cmd)
		self.telUpdater(content_id,f"Transcoding Starts FileSize={fileSize}MB")
		self.logWriter(log_file,content_id,f"Transcoding Starts FileSize={fileSize}MB")
		print(f"{self.getTime()} - Starting transcoding {fn}, FileSize={fileSize}MB")
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		# if(p.returncode != 0): status="FF-Failed"
		# else: status="Ok"
		"""cur,db=dbconn()	#Uncomment while moving to production cur.execute(f"update LOC_transcoder set isTranscoded='{status}',percentage='50%' where filename='{fn}' and app_id='{app_id}' and content_id='{content_id}';") #db.commit() #db.close()"""
		if(p.returncode != 0):
			status = "Tr-Fail"
			self.postTranscodingStatus(content_id,"Transcoding-Failed",baseUrl,err.decode('utf-8'))#?'pending', 'inprocess', 'completed', 'error', 'download', 'spending', 'QC-Failed', 'Transcoding-Failed', 'Packaging-Failed'
			self.DB_updater(content_id,app_id,fn,"transcoder",status,"11%")
			self.tmUpdater(content_id)
			self.telUpdater(content_id,"Transcoding-Failed")
			self.telUpdater(content_id,err.decode('utf-8'))
			self.logWriter(log_file,content_id,f"Transcoding-Failed {cmd}")
			return(status)
		else: status='Ok'
		#todo for GIF
		gif_dir = f"{output_dir}/output/{basefn}"
		try: os.makedirs(gif_dir)
		except: pass
		self.genGIF(f"{download_dir}/{fn}",f"{gif_dir}/preview.gif",duration)
		#todo##########
		print(f"{self.getTime()} - Transcoding completed, Status={status}")
		self.telUpdater(content_id,"Transcoding Completed")
		self.logWriter(log_file,content_id,"Transcoding Completed")
		subsInput=""

		mpdcfUrl = ""
		m3u8cfUrl = ""
		#?DASH-CENC (Widevine, PlayReady) and HLS-AES (FairPlay)
		if check_DRM == '1' or drm_nonDRM == "1":
			##'subtitle': [{'srt': 'https://sftp1.multitvsolution.com/FTP/1061/multitv/MT.srt', 'lang': 'English'}, {'srt': 'https://sftp1.multitvsolution.com/FTP/1061/multitv/MT.srt', 'lang': 'Hindi'}, {'srt': 'https://sftp1.multitvsolution.com/FTP/1061/multitv/MT.srt', 'lang': 'Urdu'}]
			dash_out_dir = f"{output_dir}/output/{basefn}/dash"
			fp_out_dir = f"{output_dir}/output/{basefn}/fp"
			try:
				os.makedirs(dash_out_dir)
				os.makedirs(fp_out_dir)
			except: pass
			if(subtitlesData != None):
			#Subtitle convert###################################################
				try:
					for subs in subtitlesData:
						srtFilePath=subs['srt']
						srt_fileLANG = subs['lang']
						srtLang=iso639.find(subs['lang'])['iso639_1']
						if ".vtt" in srtFilePath:
							print("for vtt files")
							srtFileName = self.getFile(srtFilePath,srt_fileLANG)
						else:
							srtFileName = self.getFile(srtFilePath,srt_fileLANG)
							cmd=f"srt-vtt -o {download_dir}/ {download_dir}/{srtFileName}"
							p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
							out,err=p.communicate()
							srtFileName=srtFileName.replace('srt','vtt')
						#'in=/storage/data/src/ep08_English.vtt,stream=text,init_segment=/storage/data/output/1061_6476d397010f2/dash/eng/init.mp4,segment_template=/storage/data/output/1061_6476d397010f2/dash/eng_$Number$.m4s,language=eng'
						subsInput += f"'in={download_dir}/{srtFileName},stream=text,init_segment={dash_out_dir}/{srtLang}/init.mp4,segment_template={dash_out_dir}/{srtLang}_$Number$.m4s,language={srtLang}' "
						# 	subsInput+=f"{download_dir}/{srtFileName}:lang={srtLang} " #:name={subs['lang'].capitalize()}
				except:
					print("error in srt")
					self.postTranscodingStatus(content_id,'Packaging-Failed',baseUrl,"SRT Issue")
					self.DB_updater(content_id,app_id,fn,"transcoder",status,"12%")
					self.tmUpdater(content_id)
					self.telUpdater(content_id,"SRT Issue")
					return ("Fail")
				subOpts=f"{subsInput}"
			else:
				subOpts=f"{subsInput}"
			#* todo audio segment in Packager...
			audOpts = ""
			if audioData != None:
			# AUD_inf0 = {} f"{download_dir}/{fn}"
			#/storage/data/src/1061_6454ac424bc46_mal.m4a:name=malyalam:lang=ml
				for aud in audioData:
					audFilePath = aud['srt']
					audFilelang = aud['lang'].capitalize()
					audLang = iso639.find(aud['lang'])['iso639_1']
					p_aud = Popen( f"ffmpeg -y -i {audFilePath} -c:a aac -ab 128k {download_dir}/{basefn}_{audLang}.m4a",stdout=PIPE,stderr=PIPE,shell=True)
					out,err = p_aud.communicate()
					# audOpts += f" {download_dir}/{basefn}_{audLang}.m4a:lang={audLang} " #:name={audFilelang}
					audOpts += f" 'in={download_dir}/{basefn}_{audLang}.m4a,stream=audio,init_segment={dash_out_dir}/{audFilelang}/init.mp4,segment_template={dash_out_dir}/{basefn}_{audLang}_$Number$.ts,hls_name={audLang},playlist_name={audLang}.m3u8' "
			#* todo audio segment in Packager...
			#######################################################################
			print('DRM_started')
			# drm_input = ""
			# print("content_id: ",content_id)
			self.telUpdater(content_id,"Dpackaging Started")
			self.logWriter(log_file,content_id,"Dpackaging Started")
			keyid, key = self.getDrmKey(content_id)
			if keyid == "keyerror":
				self.DB_updater(content_id,app_id,fn,"transcoder","key","11%")
				self.tmUpdater(content_id)
				self.telUpdater(content_id,"Failed Due to Key Error")
				self.logWriter(log_file,content_id,f"Key-Failed {cmd}")
				return ("fail")
			packager_cmd = f"/usr/bin/packager 'in={mp4Files[0]},stream=audio,init_segment={dash_out_dir}/audio/init.mp4,segment_template={dash_out_dir}/audio/audio_$Number$.m4s,playlist_name=audio.m3u8,drm_label=AUDIO' "
			fp_packager_cmd = f"/usr/bin/packager 'in={mp4Files[0]},stream=audio,init_segment={fp_out_dir}/audio/init.mp4,segment_template={fp_out_dir}/audio/audio_$Number$.ts,playlist_name=audio.m3u8,drm_label=AUDIO' "
			for mp4fn in mp4Files:
				vbitrate = mp4fn.split('.')[0].split('_')[-1]
				# playlists.append(f"{vbitrate}.m3u8")
				# packager_cmd += " 'in=%s,stream=video,segment_template=%s/hls/%s/%s_$Number$.ts,playlist_name=%s.m3u8' " % (mp4fn,output_dir,basefn,vbitrate,vbitrate)
				packager_cmd += f" 'in={mp4fn},stream=video,init_segment={dash_out_dir}/{vbitrate}/init.mp4,segment_template={dash_out_dir}/{vbitrate}/{vbitrate}_$Number$.m4s,playlist_name={vbitrate}.m3u8,drm_label=HD' "
				fp_packager_cmd += f" 'in={mp4fn},stream=video,init_segment={fp_out_dir}/{vbitrate}/init.mp4,segment_template={fp_out_dir}/{vbitrate}/{vbitrate}_$Number$.ts,playlist_name={vbitrate}.m3u8,drm_label=HD' "
			print("subOpts: ",subOpts)
			packager_cmd += f" {subOpts} --enable_raw_key_encryption  --keys label=AUDIO:key_id={keyid}:key={key}:iv={keyid},label=SD:key_id={keyid}:key={key}:iv={keyid},label=HD:key_id={keyid}:key={key}:iv={keyid} --protection_systems Widevine,PlayReady --generate_static_live_mpd  --mpd_output  {dash_out_dir}/master.mpd "# % (output_dir,basefn,codde)
			fp_packager_cmd += f" --enable_raw_key_encryption  --keys label=AUDIO:key_id={keyid}:key={key}:iv={keyid},label=SD:key_id={keyid}:key={key}:iv={keyid},label=HD:key_id={keyid}:key={key}:iv={keyid} --generate_static_live_hls --protection_systems FairPlay ‐‐hls_master_playlist_output {fp_out_dir}/index.m3u8 "
			print(packager_cmd)
			print(f"{self.getTime()} - Starting Packaging")
			p = Popen(packager_cmd,stdout=PIPE,stderr=PIPE,shell=True)
			out,err = p.communicate()
			if(p.returncode != 0):
				status = "P-FailD"
				self.postTranscodingStatus(content_id,'Packaging-Failed',baseUrl,err.decode('utf-8'))#?'pending', 'inprocess', 'completed', 'error', 'download', 'spending', 'QC-Failed', 'Transcoding-Failed', 'Packaging-Failed'
				self.DB_updater(content_id,app_id,fn,"transcoder",status,"12%")
				self.tmUpdater(content_id)
				self.telUpdater(content_id,"Dpackaging Failed")
				self.telUpdater(content_id,err.decode('utf-8'))
				self.logWriter(log_file,content_id,packager_cmd)
				return (status)
			else:
				status = "Ok"
			print("STATUS after PACKAGING: ",out,err)
			# for mp4fn in mp4Files: drm_input += f"{mp4fn} "
			# drm_PACKAGER = f"PallyConPackager -f --skip_pallycon_custom_info --ascending_track_order_in_manifest --site_id {site_id} --access_key {access_key} --content_id {content_id} --dash -i {drm_input} {audOpts}--fragment_duration 4 --mpd_filename master.mpd {subOpts} -o /tmp/{basefn}"
			# print(drm_PACKAGER)
			# print(f"{self.getTime()} - Starting Packaging")
			# p = Popen(drm_PACKAGER,stdout=PIPE,stderr=PIPE,shell=True)
			# out,errdd = p.communicate()
			# print(out,errdd)
			# destination = f"{output_dir}/output/{basefn}/"
			# try: os.makedirs(destination)
			# except: pass
			# if(os.path.exists(destination) == True):
			# 	src = f"/tmp/{basefn}/*"
			# else:
			# 	src = f"/tmp/{basefn}/"
			# #shutil.move(src,destination,dirs_exist_ok=False)
			# cp_cmd = f"cp -rvf {src} {destination}"
			# print(cp_cmd)
			# p = Popen(cp_cmd,stdout=PIPE,stderr=PIPE,shell=True)
			# out,err = p.communicate()
			# # print(out,err)
			# status = "P-Failed" if(p.returncode != 0) else "Ok"
			# if(p.returncode != 0):
			# 	status = "P-FailD"
			# 	self.postTranscodingStatus(content_id,'Packaging-Failed',baseUrl,errdd.decode('utf-8'))#?'pending', 'inprocess', 'completed', 'error', 'download', 'spending', 'QC-Failed', 'Transcoding-Failed', 'Packaging-Failed'
			# 	self.DB_updater(content_id,app_id,fn,"transcoder",status,"12%")
			# 	self.tmUpdater(content_id)
			# 	return (status)
			# else: status = "Ok"
			mpdcfUrl = f"{cfUrl}/multitv/output/{basefn}/dash/master.mpd" if upload_LOC == "aws" else f"{httpcfurl}/multitv/output/{basefn}/dash/master.mpd"
			os.system(f"sed -i '2d' {output_dir}/output/{basefn}/dash/master.mpd")
			#todo sed -i '2d' /storage/data/output/1061_646c87df580b4/dash/master.mpd
			self.telUpdater(content_id,"Dpackaging Completes")
		else : print("DRM ELSE ",check_DRM ,">>",drm_nonDRM)
		subsInput = ""
		if check_DRM == '0' or drm_nonDRM == "1":
			subOpts= ""
			print('Non DRM Started')
			hls_out_dir = f"{output_dir}/output/{basefn}/hls"
			try: os.makedirs(hls_out_dir)
			except: pass
			if(subtitlesData != None):
				for subs in subtitlesData:
					srtFilePath = subs['srt']
					srt_fileLANG = subs['lang']
					srtLang = iso639.find(subs['lang'])['iso639_2_b']
					if ".vtt" in srtFilePath:
						print("for vtt files")
						srtFileName = self.getFile(srtFilePath,srt_fileLANG)
					else:
						srtFileName = self.getFile(srtFilePath,srt_fileLANG)
						cmd=f"srt-vtt -o {download_dir}/ {download_dir}/{srtFileName}"
						p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
						out,err=p.communicate()
						srtFileName=srtFileName.replace('srt','vtt')
					#subsInput+=f"{download_dir}/{srtFileName}:name={subs['lang']}:lang={srtLang} "
					#segment_template={output_dir}/{basefn}/{srtLang}_$Number$.vtt  ##todo {output_dir}/hls/{basefn}/
					# subsInput += f"'in={download_dir}/{srtFileName},stream=text,segment_template={output_dir}/hls/{basefn}/{srtLang}_$Number$.vtt,playlist_name={srtLang}_sub.m3u8,hls_group_id=text,hls_name={subs['lang'].capitalize()}' "
					subsInput += f"'in={download_dir}/{srtFileName},stream=text,segment_template={hls_out_dir}/{srtLang}_$Number$.vtt,playlist_name={srtLang}_sub.m3u8,hls_group_id=text,hls_name={srtLang}' "
					print(subsInput)
				subOpts = subsInput
			else:
				subOpts = ""
			#* todo audio segment in Packager...
			audOpts = ""
			if audioData != None:
			# AUD_inf0 = {} f"{download_dir}/{fn}"
				for aud in audioData:
					audFilePath = aud['srt']
					audFilelang = aud['lang'].capitalize()
					audLang = iso639.find(aud['lang'])['iso639_2_b']
					p_aud = Popen( f"ffmpeg -y -i {audFilePath} -c:a aac -ab 128k {download_dir}/{basefn}_{audLang}.m4a",stdout=PIPE,stderr=PIPE,shell=True)
					out,err = p_aud.communicate()
					# 'in=/storage/data/mp4/mal_test.m4a,stream=audio,segment_template=/storage/data/hls/1061_6454ac424bc46/mal_$Number$.ts,playlist_name=mal.m3u8'
					# audOpts += f" 'in={download_dir}/{basefn}_{audLang}.m4a,stream=audio,segment_template={output_dir}/hls/{basefn}/{basefn}_{audLang}_$Number$.ts,hls_name={audFilelang},playlist_name={audLang}.m3u8' "
					audOpts += f" 'in={download_dir}/{basefn}_{audLang}.m4a,stream=audio,segment_template={hls_out_dir}/{basefn}_{audLang}_$Number$.ts,hls_name={audLang},playlist_name={audLang}.m3u8' "
			#* todo audio segment in Packager...
			packager_cmd = "/usr/bin/packager "
			self.telUpdater(content_id,"Packaging Started")
			self.logWriter(log_file,content_id,"Packaging Started")
			master_hlsNAME = f"master_{''.join(random.choices(string.ascii_letters, k=16))}.m3u8"
			playlists = [master_hlsNAME]
			for mp4fn in mp4Files:
				vbitrate = mp4fn.split('.')[0].split('_')[-1]
				playlists.append(f"{vbitrate}.m3u8")
				# packager_cmd += " 'in=%s,stream=video,segment_template=%s/hls/%s/%s_$Number$.ts,playlist_name=%s.m3u8' " % (mp4fn,output_dir,basefn,vbitrate,vbitrate)
				packager_cmd += f" 'in={mp4fn},stream=video,segment_template={hls_out_dir}/{vbitrate}_$Number$.ts,playlist_name={vbitrate}.m3u8' " # % (,,,,)
			try:
				default_lang = os.popen(f"ffprobe -v error -show_entries stream=index:stream_tags=language -select_streams a -of compact=p=0:nk=1 {download_dir}/{fn}").read().split("|")[1].strip() #todo must
				packager_cmd += f" 'in={mp4fn},stream=1,segment_template={hls_out_dir}/$Number$.aac,hls_name={default_lang},playlist_name={default_lang}.m3u8' "
				playlists.append(f"{default_lang}.m3u8")
			except:
				print("No specific lang")
				default_lang = "hin"
				packager_cmd += f" 'in={mp4fn},stream=1,segment_template={hls_out_dir}/$Number$.aac,hls_name={default_lang},playlist_name={default_lang}.m3u8' "
				playlists.append(f"{default_lang}.m3u8")
			print("subOpts: ",subOpts)
			packager_cmd += f" {subOpts} {audOpts}"
			# print("subOpts: ",subOpts)
			# packager_cmd += f" {subOpts} {audOpts}"
			
			packager_cmd += f" --segment_duration 4 --hls_master_playlist_output {hls_out_dir}/{master_hlsNAME} "# % (output_dir,basefn,codde)
			print(packager_cmd)
			print(f"{self.getTime()} - Starting Packaging")
			p = Popen(packager_cmd,stdout=PIPE,stderr=PIPE,shell=True)
			out,err = p.communicate()
			if(p.returncode != 0):
				status = "P-Fail"
				self.postTranscodingStatus(content_id,'Packaging-Failed',baseUrl,err.decode('utf-8'))#?'pending', 'inprocess', 'completed', 'error', 'download', 'spending', 'QC-Failed', 'Transcoding-Failed', 'Packaging-Failed'
				self.DB_updater(content_id,app_id,fn,"transcoder",status,"12%")
				self.tmUpdater(content_id)
				self.telUpdater(content_id,"Packaging Failed")
				self.telUpdater(content_id,err.decode('utf-8'))
				self.logWriter(log_file,content_id,packager_cmd)
				return (status)
			else:
				status = "Ok"
			print("STATUS after PACKAGING: ",out,err)
			##todo DASH Creation##
			# packager_cmd = "/usr/bin/packager "  # try: # 	os.makedirs("%s/hls/%s" % (output_dir,basefn)) # 	os.makedirs("%s/dash/%s" % (output_dir,basefn)) # except: pass # playlists=['master.m3u8','eng.m3u8'] # for mp4fn in mp4Files: # 	vbitrate = mp4fn.split('.')[0].split('_')[-1] # 	playlists.append(f"{vbitrate}.m3u8") #packager_cmd+="'in=%s,stream=video,init_segment=h264_%s/init.mp4,segment_template=%s/dash/%s/%s_$Number$.m4s,playlist_name=%s.m3u8' " % (mp4fn,vbitrate,output_dir,basefn,vbitrate,vbitrate) # 	packager_cmd += f"'in={mp4fn},stream=video,init_segment={output_dir}/dash/{basefn}/init_{vbitrate}.mp4,segment_template={output_dir}/dash/{basefn}/{vbitrate}_$Number$.m4s,playlist_name={vbitrate}.m3u8' " # packager_cmd += f"'in={mp4fn},stream=1,init_segment={output_dir}/dash/{basefn}/aud_init.mp4,segment_template=output_dir/dash/basefn/$Number$.m4s,language=eng,hls_name=eng,playlist_name=eng.m4s' " # packager_cmd += f" --segment_duration 4 --mpd_output {output_dir}/dash/{basefn}/master.mpd " # #print(packager_cmd)
			##todo DASH Creation##
			print(f"{self.getTime()} - Completed Packaging: {status}")
			for playlist in playlists:
				self.sortPlaylist(f"{output_dir}/output/{basefn}/hls/{playlist}")
			m3u8cfUrl = f"{cfUrl}/multitv/output/{basefn}/hls/{master_hlsNAME}" if upload_LOC == "aws" else f"{cfUrl}/multitv/output/{basefn}/hls/{master_hlsNAME}"
			self.telUpdater(content_id,"Packaging Completed")
		else : print("Non DRM ELSE ",check_DRM ,">>",drm_nonDRM)
		gifURL = f"{httpcfurl}/multitv/output/{basefn}/preview.gif" if upload_LOC == "aws" else f"{httpcfurl}/multitv/output/{basefn}/preview.gif"#https://ott1061.s3.ap-south-1.amazonaws.com/multitv/output/HLS/1061_63a45144c25fc/preview.gif
		thumbURL = f"{httpcfurl}/multitv/output/{basefn}/master.png" if upload_LOC == "aws" else f"{httpcfurl}/multitv/output/{basefn}/master.png"		
		print(f"{self.getTime()} - Packaging completed, Status={status}")
		#todo##########################
		self.genThumb(output_dir,basefn,mp4fn,duration)
		self.DB_updater(content_id,app_id,fn,"transcoder",status,"75%")
		# cur,db = dbconn() # cur.execute(f"update LOC_transcoder set isTranscoded='{status}',percentage='75%' where filename='{fn}' and app_id='{app_id}' and content_id='{content_id}';") # db.commit() # db.close()
		#todo##########################

		# if(p.returncode != 0): # 	status = "Packaging-Failed" # 	self.postTranscodingStatus(content_id,status,baseUrl)  # 	return(status) #self.sortPlaylist("%s/hls/%s/master.m3u8" % (output_dir,basefn))
		# self.genThumb(output_dir,basefn,mp4fn,duration)
		uploadDir = "%s/output/%s" % (output_dir,basefn)
		# upload_hls = self.upload(bucket,uploadDir,basefn,fn)
		#todo##################
		if upload_LOC == "aws":
			print("uploading to AWS")
			upload_hls = self.upload(bucket,uploadDir,basefn,fn)
			payload={'path': f'multitv/output/{basefn}', 'app_id':app_id}
			response = post(f"https://{baseUrl}/api/invalidator", data=payload)
			print("invalidatee: ",response.text)
		elif upload_LOC == "netstorage":
			print("Uploading to Netstorage")
			upload_hls = self.upload_netstorage(bucket,uploadDir,basefn,fn,NS_CPCODE,NS_KEY,NS_KEYNAME,NS_HOSTNAME)
		#todo##################
		if(upload_hls is True):
			status='Ok'
			print(f"{self.getTime()} - Uploaded")
		else:
			status='Up-Fail'
			print(f"{self.getTime()} - Upload Failed")
			self.DB_updater(content_id,app_id,fn,"uploader",status,"99%")
		#todo#########################
		self.DB_updater(content_id,app_id,fn,"uploader",status,"99%")
		# cur,db = dbconn() # cur.execute(f"update LOC_transcoder set isUploaded='{status}',percentage='99%',spriteGen='0' where filename='{fn}' and app_id='{app_id}' and content_id='{content_id}';") # db.commit() # db.close()
		#todo########################
		if drm_nonDRM == "1":
			self.postEncodeStatusBothnonandnonDRM(content_id,duration,m3u8cfUrl,mpdcfUrl,baseUrl,gifURL,thumbURL,keyid)
		elif drm_nonDRM == "0":
			cfURL = m3u8cfUrl if check_DRM == "0" else mpdcfUrl
			print("cfURL",cfURL)
			keyid=""
			self.postEncodeStatusBothnonandnonDRM(content_id,duration,cfURL,cfURL,baseUrl,gifURL,thumbURL,keyid) 
		else: print("drm_nonDRM: ",drm_nonDRM)
		status="completed"
		self.postTranscodingStatus(content_id,status,baseUrl,status) #?'pending', 'inprocess', 'completed', 'error', 'download', 'spending', 'QC-Failed', 'Transcoding-Failed', 'Packaging-Failed'
		self.tmUpdater(content_id)
		self.telUpdater(content_id,"Completes")
		return(status)
hwdev=argv[1]
s=transcode()
s.transcoder(hwdev)

"""while True: try: s=transcode() s.transcoder(hwdev) sleep(random.randint(2, 20)) except KeyboardInterrupt: sys.exit() except Exception as e: print(e) continue"""
