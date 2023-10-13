from time import sleep
from sys import exit
from dbconn import *
from conf import *
from datetime import datetime
from subprocess import Popen, PIPE
from requests import post, get
import DownloadProgressBar, json, random, logging, urllib.parse, ast, os,iso639

class QC(object):
	def __init__(self):
		self.logfile=transcode_log
		if(os.path.exists(f"{self.logfile}") is True):
			os.makedirs(f"{self.logfile}")
		logging.basicConfig(filename="logs/qc.log", format='%(asctime)s %(message)s',filemode='w')
		self.logger = logging.getLogger()
		self.logger.setLevel(logging.DEBUG)
  
	def precheck(self):
		try:
			os.makedirs("%s/mp4" % output_dir)
			os.makedirs("%s/hls" % output_dir)
			os.makedirs(download_dir)
		except:
			pass
		return(True)

	def postTranscodingStatus(self,content_id,status,baseUrl,error_code):
		url=f"https://{baseUrl}/crons/transcodeupdate"
		# url="https://altbdev.multitvsolution.com/crons/transcodeupdate"
		body=body ={'content_id': content_id,'status':status,'error_code':error_code}
		r=post(url,json=body)
		return(True)

	def getTime(self):
		now = datetime.now()
		date=now.strftime("%Y-%m-%d %H:%M:%S")
		return(date)

	def removejsonchar(self,data):
		data=data[:-2]
		data=data[1:]
		return(data)

	def getFilemetadata(self,fn):
		cmd="ffprobe -v quiet -print_format json -show_format -show_streams %s" % (fn)
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		ffData=json.loads(out)
		for data in ffData['streams']:
			if(data['codec_type'] == 'video'):
				return(data['codec_name'],data['pix_fmt'])

	def checkAV(self,fn):
		cmd="ffprobe -v quiet -print_format json -show_format -show_streams %s" % (fn)
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		ffData=json.loads(out)
		i=1
		for data in ffData['streams']:
			print(i)
			print(data)
			if(data['codec_type'] == 'video'):
				video=1
				print("Video=%s" % video)
			else: return('NoVideo')
			print(data['codec_type'])
			if(data['codec_type' == 'audio']):
				audio=1
				print(audio)
			else: return('NoAudio')
			i+=1
		return('True')

	def checkSilence(self,fn):
		cmd="ffmpeg -i %s -af \"pan=1c|c0=c1,silencedetect=noise=-18dB:d=0.5\" -f null - 2>&1 | awk '/silence_end/ && ($5 == $8) {print \"silent\"}'" % (fn)
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		silencestatus=out.decode('utf-8')
		if(silencestatus == 'silent'): return('True')
		else: return('False')

	def DB_updaterQC(self,content_id,app_id,value,trans_details):
		payload={'content_id': content_id,'app_id': app_id,'value': value,'trans_details':trans_details}
		response = post(db_update_API, data=payload)
		print(response,response.text)
		return response.text

	def file_updaterQC(self,content_id,app_id,fn,value):
		payload={'content_id': content_id,'app_id': app_id,'file_name': fn,'value': value}
		response = post(qc_fileupdate, data=payload)
		print(response,response.text)
		return response.text

	def QC_finalUpdate(self,content_id,app_id,fn,gpuvalue,qcc):
		payload={'content_id': content_id,'app_id': app_id,'file_name': fn,'qcc': qcc,'gpuvalue':gpuvalue}
		response = post(QC_finalUpdateAPI, data=payload)
		print(response,response.text)
		return response.text

	def getFile(self):
		#todo$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
		job_data = get(job_API)
		# print(job_data,job_data.reason,job_data.text,type(job_data.text))
		if job_data.text == "No Data": 
			print(f"{self.getTime()} - Nothing to Do")
			return ("False","False","False","False")
		else:
			print(job_data.text)
			js_data = json.loads(job_data.text)
			app_id, content_id, path, filename = js_data['dbdump'][0]['app_id'], js_data['dbdump'][0]["content_id"], js_data['dbdump'][0]["path"], js_data['dbdump'][0]["filename"]
			# app_id,content_id,path,filename,gpu_compatible = js_data['dbdump'][0]['app_id'],js_data['dbdump'][0]["content_id"],js_data['dbdump'][0]["path"],js_data['dbdump'][0]["filename"],js_data['dbdump'][0]["gpu_compatible"]
		# cur,db=dbconn() # cur.execute("select app_id,content_id,path from LOC_transcoder where qc='0' limit 0,1;") # dbData=cur.fetchone() # if(dbData is not None):  # 	app_id,content_id,path=dbData # else: # 	db.close() # 	print(f"{self.getTime()} - Nothing to Do") # 	return('False','','') #  db.close()
		#todo$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
		#todo$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
		self.DB_updaterQC(content_id,app_id,"-1",trans_details)
		# cur,db=dbconn() # cur.execute(f"update LOC_transcoder set qc='-1' where app_id='{app_id}' and content_id='{content_id}';") # db.commit()
		#todo$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

		self.logger.debug(f"Starting processing {app_id} json={path}")
		#todo$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
		# print(f'Analysing json: {path}') # f=open(path,'r') # data=f.read() # f.close() # data=ast.literal_eval(data) # data=data['content_id']
		print(type(js_data))
		data = ast.literal_eval(js_data['j_data'])['content_id']
		#todo$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

		#video_file_path=data[0]["video_file_name"].split('/')[:-1]
		if('+' in data[0]["video_file_name"].rsplit('/',1)[1]):
			encodedFn=data[0]["video_file_name"].rsplit('/',1)[1].replace('+',' ')
		if(' ' in data[0]["video_file_name"].rsplit('/',1)[1]):
			encodedFn=urllib.parse.quote(data[0]["video_file_name"].rsplit('/',1)[1])
		else:
			encodedFn=data[0]["video_file_name"].rsplit('/',1)[1]
		video_file_path="%s/%s" % (data[0]["video_file_name"].rsplit('/',1)[0],encodedFn)
		video_file_path=video_file_path.replace(' ','%20')
		content_id=data[0]["content_id"]
		baseUrl=data[0]['base_url']
		video_file_name=data[0]["name"] #video_file_path.split('/')[-1]
		print(f"{self.getTime()} - Downloading {video_file_path}")
		downloadFn=f"{download_dir}/{video_file_name}"
		self.logger.debug(f"Downloading {video_file_path} as {downloadFn}")
		try:
			DownloadProgressBar.download_url(video_file_path,downloadFn)
		except:
			pass
		
		#* CODE FOR AUDIO DURATION CHECKING start
		try:
			audioData = data[0]['audio'] if data[0]['audio'] != '' else None
		except:
			audioData = None
		AUD_inf0 = {}
		if audioData != None:
			# AUD_inf0 = {}
			for aud in audioData:
				audFilePath = aud['srt']
				audFilelang = aud['lang']
				audLang = iso639.find(aud['lang'])['iso639_2_b']
				# print(audFilePath,audFilelang)
				dura = os.popen(f"ffprobe -i {audFilePath} -show_entries format=duration -v quiet -of csv='p=0'").read()
				# print(type(dura))#print(type(audLang))
				AUD_inf0[audLang] = int(float(dura))

		#* CODE FOR AUDIO DURATION CHECKING ends

		if(os.path.exists(downloadFn) is True):
			if audioData != None:
				video_dura = os.popen(f"ffprobe -i {downloadFn} -show_entries format=duration -v quiet -of csv='p=0'").read()
				for val in AUD_inf0.values():
					diff_dur = int(float(video_dura))-val
					if diff_dur == 0: print("finee")
					else:
						self.file_updaterQC(content_id,app_id,video_file_name,"NA")
						return('False','','','')
						
			#todo $$$$$$$$$$$$$$$$$$$$$$$$$$$$
			self.file_updaterQC(content_id,app_id,video_file_name,"-1")
			# cur,db=dbconn() # cur.execute(f"update LOC_transcoder set filename='{video_file_name}' where app_id='{app_id}' and content_id='{content_id}';") # db.commit()
			#todo $$$$$$$$$$$$$$$$$$$$$$$$$$$$
			self.logger.debug(f"Download {downloadFn} successful")
			return(video_file_name,app_id,content_id,baseUrl)
		else:
			#todo $$$$$$$$$$$$$$$$$$$$$$$$$$$$
			self.file_updaterQC(content_id,app_id,video_file_name,'404')
			self.postTranscodingStatus(content_id,"download",baseUrl,"Download error 404") #?'pending', 'inprocess', 'completed', 'error', 'download', 'spending', 'QC-Failed', 'Transcoding-Failed', 'Packaging-Failed'
			# cur,db=dbconn() # cur.execute(f"update LOC_transcoder set filename='{video_file_name}',qc='404' where app_id='{app_id}' and content_id='{content_id}';") # db.commit()
			#todo $$$$$$$$$$$$$$$$$$$$$$$$$$$$
			self.logger.debug(f"Download failed {downloadFn}")
			return('False','','','')

	def qc(self,fn,app_id,content_id,baseUrl):
		gpu_compatible=False
		downloadFn=f"{download_dir}/{fn}"
		cmd="ffmpeg -v error -i \"%s\" -codec copy -f null -" % (downloadFn)
		self.logger.debug(f"{cmd}")
		print(f"{self.getTime()} - Analyzing {fn}")
		self.logger.debug(f"Analysing {downloadFn}")
		p=Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
		out,err=p.communicate()
		if(err.decode('utf-8') == ''):
			qc = 'Ok'
			if downloadFn.endswith('.mp3'):
				print("for mp3")
				gpu_compatible = False
			else:
				codec_name,pix_fmt=self.getFilemetadata(downloadFn)
				if(codec_name == 'h264' or codec_name == 'mpeg2video' and pix_fmt == 'yuv420p'):
					gpu_compatible=True
			self.postTranscodingStatus(content_id,"inprocess",baseUrl,'InProcess')
		else:
			qc='Failed'

		#todo $$$$$$$$$$$$$$$$$$$$$$$$$$$$
		self.QC_finalUpdate(content_id,app_id,fn,gpu_compatible,qc)
		#todo $$$$$$$$$$$$$$$$$$$$$$$$$$$$
		
		if(qc == 'Failed'):
			status="QC-Failed"
			self.postTranscodingStatus(content_id,status,baseUrl,err.decode('utf-8'))  #?'pending', 'inprocess', 'completed', 'error', 'download', 'spending', 'QC-Failed', 'Transcoding-Failed', 'Packaging-Failed'
			return(status)
		return(True)

s=QC()
s.precheck()
downloadFile,app_id,content_id,baseUrl=s.getFile()
if(downloadFile != 'False'):	s.qc(downloadFile,app_id,content_id,baseUrl)
# while True: # 	try: # 		s=QC() # s.precheck() # 		downloadFile,app_id,content_id,baseUrl=s.getFile() # 		if(downloadFile != 'False'):	s.qc(downloadFile,app_id,content_id,baseUrl) # 		sleep(random.randint(2, 10)) # 	except KeyboardInterrupt: # 		exit() # 	except Exception as e: # 		print(e) # 		continue