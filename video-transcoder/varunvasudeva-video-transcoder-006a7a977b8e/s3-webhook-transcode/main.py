#Script to transcode video once uploaded in s3, Must be called from SNS service.
#Written by: Varun
#Date: 14-10-2022
#v1.0

import bjoern
import json
from paste.urlmap import URLMap
from paste import request
from datetime import datetime
from dbconn import *
import os, sys
from conf import *
from time import sleep
import requests

def pti(environ,start_response):      #Listen to SNS webhook json and insert the required information in database
		status = '200 OK'
		response_body=b"status ok"
		response_headers = [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', "*")]
		readbytes=environ['wsgi.input'].read()
		readstr = readbytes.decode('utf-8')
		start_response(status,response_headers)
		msg=json.loads(readstr)
		msg=json.loads(msg['Message'])
		if(msg['detail-type'] != 'Object Created'): return(response_body)	#Ignore all other SNS events
		bucketName=msg['detail']['bucket']['name']
		filePath,fn=str(msg['detail']['object']['key']).rsplit('/',1)
		#print(filePath,fn)
		if('Thumbnails' in filePath):  return(response_body)	#Ignore all files in Thumbnails
		filesize=int(msg['detail']['object']['size'])/1024/1024
		filesize="%.2f" % filesize
		cur,db=dbconn()
		now = datetime.now()
		date=now.strftime("%Y%m%d")
		dt = now.strftime("%Y/%m/%d %H:%M:%S")
		qc='0'
		isTranscoded='0'
		isUploaded='0'
		logging="%s,Bucket=%s,File=%s,Size=%s" % (dt,bucketName,fn,filesize)
		if(os.path.exists(f"{webhooklog}") is False):
			os.makedirs(f"{webhooklog}")
		f=open(f"{webhooklog}/{date}.log",'a+')
		f.write(logging)
		f.close()
		print(logging)
		query="insert into s3transcoder(dt,bucketName,path,qc,isTranscoded,filename,isUploaded) values('%s','%s','%s','%s','%s','%s','%s') on duplicate key update dt='%s',bucketname='%s',path='%s',qc='%s',isTranscoded='%s',isUploaded=%s" % (dt,bucketName,filePath,qc,isTranscoded,fn,isUploaded,dt,bucketName,filePath,qc,isTranscoded,isUploaded)
		#print(query)
		if(fn.endswith('.filepart') is False):
			cur.execute(query)
			url=f"{apiURL}/uploaded-clips"
			Headers={"Content-Type": "application/json"}
			Data=[]
			val={}
			val['clips_name']=fn
			Data.append(val)
			r=requests.post(url,headers=Headers, data=json.dumps(Data))
			response=json.loads(r.text)
			print(r.text)
			clips_id=response['clips_id']
			query1=f"update s3transcoder set clips_id='{clips_id}',file_size='{filesize} MB' where filename='{fn}';"
			cur.execute(query1)
			db.commit()
			"""Data=[]
			val={}
			val['clips_id']=clips_id
			val['clips_name']=fn
			val['file_size']=filesize
			val['uploaded_time']=dt
			val['status']='queued'
			Data.append(val)
			r=requests.post(url,headers=Headers, data=json.dumps(Data))
			print(r.text)"""
		else:
			print(f"{dt}-Dropped {fn} because of wrong file format")
		db.close()
		return(response_body)

def status(environ,start_response):      #Listen to SNS webhook json and insert the required information in database
		status = '200 OK'
		response_body=b"status ok"
		response_headers = [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', "*")]
		start_response(status,response_headers)
		return(response_body)

#API Functions
map_app = URLMap({})
map_app['/pti'] = pti
map_app['/status'] = status

bjoern.listen(map_app, '0.0.0.0', 80)
while True:
	try:
		bjoern.run()
	except KeyboardInterrupt:
		print("Keyboard Interrupt")
		sys.exit()
	except Exception as e:
		print(e)
		continue