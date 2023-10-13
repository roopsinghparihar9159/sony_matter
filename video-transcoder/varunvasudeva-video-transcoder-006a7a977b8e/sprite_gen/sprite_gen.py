# from email.mime import base
from dbconn import *
from conf import *
from subprocess import PIPE, Popen
from datetime import datetime
# from time import sleep
import ast, os, boto3, glob,json #, sys #, json, m3u8, re,
from requests import post,get
from akamai.netstorage import Netstorage

class sprite(object):
	def __init__(self):
		self.logfile=transcode_log
		if(os.path.exists(f"{self.logfile}") is True): os.makedirs(f"{self.logfile}")

	def getTime(self):
		now = datetime.now()
		date = now.strftime("%Y-%m-%d %H:%M:%S")
		return(date)

	def removejsonchar(self,data):
		data = data[:-2]
		data = data[1:]
		return(data)

	def upload(self,bucketName,uploadFn,baseFn):
		s3 = boto3.client('s3')
		cmd = "/usr/local/bin/aws s3 sync %s s3://%s/multitv/output/HLS/%s/" % (uploadFn,bucketName,baseFn)
		print(cmd)
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err = p.communicate()
		err = err.decode('utf-8')
		if(err != ''): return(False)
		else: return(True)
  
	def upload_netstorage(self,bucketName,uploaddir,NS_CPCODE,NS_KEY,NS_KEYNAME,NS_HOSTNAME):
		print("uploading to netstorage")
		ns = Netstorage(NS_HOSTNAME, NS_KEYNAME, NS_KEY, ssl=False)
		for filename in glob.iglob(uploaddir+"/**", recursive=True):
    		# print(filename if "." in filename else None)
				local_source = filename if "sprite_tv.jpg" in filename else (filename if "sprite_web.jpg" in filename else None)
				if local_source != None:
					destination_FN = local_source.replace("/storage/data/","")
					netstorage_destination = f"/{NS_CPCODE}/{bucketName}/{destination_FN}"
					print("LOCAL SOURCE: ",local_source," DESTINATION: ",netstorage_destination)
					ok, response = ns.upload(local_source, netstorage_destination)
					print( ok, " -- ",response)
		print( ok, " -- ",response)
		if(ok == True): return(True)
		else: return(False)

	def postSpriteStatus(self,content_id,cfTVURL,cfWebURL,baseUrl):
		url=f"https://{baseUrl}/crons/updatesprite_url"
		# url = "https://altbdev.multitvsolution.com/crons/updatesprite_url"
		body = {'content_id': content_id,'sprite_web':cfWebURL,'sprite_tv':cfTVURL}
		r = post(url,json=body)
		if(r.status_code == 200): return(True)
		else: return(False)
	
	def DB_updater(self,content_id,app_id,file_name,typee,value,percentage):
		payload={'content_id': content_id,'app_id': app_id,'file_name': file_name,'typee': typee,'value': value,'percentage': percentage}
		response = post(db_update_API, data=payload)
		print(response,response.text)
		return response.text	

	def Sprite(self):
		#todo #############################
		job_data = get(job_API%trans_details)
		# print(job_data,job_data.reason,job_data.text,type(job_data.text))
		if job_data.text == "No Data": 
			print(f"{self.getTime()} - Nothing to Do")
			return (False)
		else:
			js_data = json.loads(job_data.text)
			app_id,content_id,path,filename,gpu_compatible = js_data['dbdump'][0]['app_id'],js_data['dbdump'][0]["content_id"],js_data['dbdump'][0]["path"],js_data['dbdump'][0]["filename"],js_data['dbdump'][0]["gpu_compatible"]
		# cur,db=dbconn() # cur.execute("select app_id,content_id,path,filename,gpu_compatible from LOC_transcoder where isTranscoded='Ok' and qc='Ok' and isUploaded='Ok' and spriteGen='0' limit 0,1;") # dbData=cur.fetchone() # if(dbData is not None):  # 	app_id, content_id, path, filename, gpu_compatible = dbData # 	print(f"{self.getTime()} - Creating sprite {filename}") # else: # 	db.close() # 	print(f"{self.getTime()} - Nothing to Do") # 	return(False) # db.close()
		#todo ################################
		#todo ################################
		self.DB_updater(content_id,app_id,filename,"sprite_gen","-1","80%")
		# cur,db = dbconn() # cur.execute(f"update LOC_transcoder set spriteGen='-1' where filename='{filename}' and app_id='{app_id}' and content_id='{content_id}';") # db.commit() # db.close()
		#todo ################################
		#todo ################################
		# f = open(path,'r') # data = f.read() # f.close() # #data=ast.literal_eval(self.removejsonchar(data)) # data = ast.literal_eval(data) # data = data['content_id']
		data = js_data['j_data']['content_id']
		#todo ################################
		baseFn = filename.split(".")[0]
		upload_LOC = data[0]['upload_key'] if 'upload_key' in data[0] else "aws"
		mx_BR = []
		for flavor in data:
			vbitrate=flavor['vb'].replace('k','000')
			mx_BR.append(int(vbitrate))
			bucketName = flavor['bucket']
			NS_CPCODE=flavor["cp_code"] if 'cp_code' in flavor else ""
			NS_KEY=flavor["netstorage_key"] if 'netstorage_key' in flavor else ""
			NS_KEYNAME=flavor["netstorage_keyName"] if 'netstorage_keyName' in flavor else ""
			NS_HOSTNAME=flavor["ns_host"] if 'ns_host' in flavor else ""
			content_id = flavor['content_id']
			cfUrl = flavor['cloudfront']
			htpscfurl = flavor['cloudfront']
			baseUrl=flavor['base_url']
		cfUrl = f"{cfUrl}/multitv/output/HLS/{baseFn}"# if upload_LOC == "aws" else f"{cfUrl}/multitv/hls/{basefn}/master.m3u8"
		bit_Rt = min(mx_BR)
		mp4dir = f"{output_dir}/mp4/{baseFn}_{bit_Rt}.mp4"
		if os.path.exists(path):
			Mobile_res = "224 127" #"19200x216"
			TV_res = "640 360" #"64000x360"
			interval = 5
			columns = 10
			sprt_ot = f"sprite_web.jpg"
			sprt_ot_tv = f"sprite_tv.jpg"
			gen_cm = f"./generator {mp4dir} {interval} {Mobile_res} {columns} {output_dir}/output/{baseFn}/{sprt_ot}"
			gen_cm_tv = f"./generator {mp4dir} {interval} {TV_res} {columns} {output_dir}/output/{baseFn}/{sprt_ot_tv}"
			print(gen_cm)
			print(gen_cm_tv)
			p = Popen(gen_cm,stdout=PIPE,stderr=PIPE,shell=True)
			out,err = p.communicate()
			print(out,err)
			if(p.returncode != 0):
				status = "Failed"
				print(f"{self.getTime()} - Mobile Sprite failed")
			else:
				status = "Ok"
				print(f"{self.getTime()} - Mobile Sprite Created")
				cfWebURL = f"{cfUrl}/sprite_web.jpg" if upload_LOC == "aws" else f"{htpscfurl}/multitv/output/{baseFn}/sprite_web.jpg"
			p = Popen(gen_cm_tv,stdout=PIPE,stderr=PIPE,shell=True)
			out,err = p.communicate()
			print(out,err)
			if(p.returncode != 0):
				status = "Failed"
				print(f"{self.getTime()} - TV Sprite failed")
			else:
				status = "Ok"
				print(f"{self.getTime()} - TV Sprite Created")
				cfTVURL = f"{cfUrl}/sprite_tv.jpg"  if upload_LOC == "aws" else f"{htpscfurl}/multitv/output/{baseFn}/sprite_tv.jpg"
			uploadFn = f"{output_dir}/output/{baseFn}"
			# upload = self.upload(bucketName,uploadFn,baseFn)
			#todo##################
			if upload_LOC == "aws":
				print("uploading to AWS")
				upload = self.upload(bucketName,uploadFn,baseFn)
			elif upload_LOC == "netstorage":
				print("Uploading to Netstorage")
				upload = self.upload_netstorage(bucketName,uploadFn,NS_CPCODE,NS_KEY,NS_KEYNAME,NS_HOSTNAME)
			#todo##################
			apiPost = self.postSpriteStatus(content_id,cfTVURL,cfWebURL,baseUrl)
			if(apiPost == False):	status="API500"
			print(f"{self.getTime()} - Sprite completed, Status={status},Upload={upload},APIResponse={apiPost}")
			
   			#todo ######################
			self.DB_updater(content_id,app_id,filename,"sprite_gen",status,"100%")
			# cur,db = dbconn() # cur.execute(f"update LOC_transcoder set spriteGen='{status}',percentage='100%' where filename='{filename}' and app_id='{app_id}' and content_id='{content_id}';") # db.commit() # db.close()
			#todo ######################

			return(status)
		else: print("No MP4 file found")

s=sprite()
s.Sprite()

"""while True: try: s=sprite() s.Sprite() sleep(10) except KeyboardInterrupt: sys.exit() except Exception as e: print(e) continue"""