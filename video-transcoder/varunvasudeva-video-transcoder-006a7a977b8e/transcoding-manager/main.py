from flask import Flask, request, Response
from dbconn import *
import json
#from datetime import datetime, date
import datetime
import os

app = Flask(__name__)
app.debug=True

@app.route('/pti-octopus-list',methods=['GET','POST'])
def ptiOctopusList():
	if(request.method == 'POST'):
		lowerlimit=request.form['lowerlimit']
		upperlimit=request.form['upperlimit']
		try:
			dt=request.form['date']
		except:
			dt=datetime.date.today()
	cur,db=dbconn()
	if(upperlimit == '0'):
		limitParams=""
	else:
		limitParams=f"limit {lowerlimit},{upperlimit}"
	query=f"select dt,filename,qc,isTranscoded,isUploaded,completition_time,clips_id,file_size from s3transcoder where dt like '{dt}%' order by dt desc {limitParams};"
	cur.execute(query)
	data=cur.fetchall()
	db.close()
	datadump=[]
	for row in data:
		val={}
		date,filename,qc,isTranscoded,isUploaded,completition_time,clips_id,file_size=row
		val['date']=date.strftime("%Y-%m-%d %H:%M")
		val['filename']=filename
		val['qc']=qc
		val['isTranscoded']=isTranscoded
		val['isUploaded']=isUploaded
		try:
			val['completion_time']=completition_time.strftime("%Y-%m-%d %H:%M")
		except:
			val['completion_time']='NA'
		val['clips_id']=clips_id
		val['file_size']=file_size
		datadump.append(val)
	resp = Response(response=json.dumps(datadump), status=200,  mimetype="application/json")
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp

@app.route('/pti-octopus-action',methods=['GET','POST'])
def ptiOctopusAction():
	if(request.method == 'POST'):
		clips_id=request.form['clips_id']
		action=request.form['action'] #0=Retranscode, 1=Delete
		cur,db=dbconn()
		if(action == '0'):
			query=f"update s3transcoder set qc='0',isTranscoded='0' where clips_id='{clips_id}';"
		elif(action == '1'):

			query=f"delete from s3transcoder where clips_id='{clips_id}' and qc<>'Ok';"
		cur.execute(query)
		db.commit()
		affectedRows=db.affected_rows()
		db.close()
		if(affectedRows == 0):
			datadump={'status':'ID Already queued'}
		else:
			datadump={'status':'True'}
		resp = Response(response=json.dumps(datadump), status=200, mimetype="application/json")
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp

@app.route('/pti-transcoding-list',methods=['GET','POST'])
def ptiTranscodingList():
	if(request.method == 'POST'):
		lowerlimit=request.form['lowerlimit']
		upperlimit=request.form['upperlimit']
		try:
			dt=request.form['date']
		except:
			dt=datetime.date.today()
	cur,db=dbconn()
	if(upperlimit == '0'):
		limitParams=""
	else:
		limitParams=f"limit {lowerlimit},{upperlimit}"
	query=f"select arrival_dt,filename,status,completed_dt,duration from ptirecoder where arrival_dt like '{dt}%' and type='r' order by arrival_dt desc {limitParams};"
	print(query)
	cur.execute(query)
	data=cur.fetchall()
	db.close()
	datadump=[]
	for row in data:
		val={}
		date,filename,status,completition_time,duration=row
		val['date']=date.strftime("%Y-%m-%d %H:%M")
		file_size=os.stat(f"/storage/FTP/PTI/{filename}")
		file_size=file_size.st_size/(1024 * 1024)
		file_size=round(file_size,2)
		val['filename']=filename.split('/')[-1].split('-')[1]
		if(status == '1'):
			val['qc']='Ok'
			val['isTranscoded']='Ok'
		elif(status == '-1'):
			val['qc']='Ok'
			val['isTranscoded']='Queued'
		val['file_size']='0'
		val['duration']=duration
		try:
			val['completion_time']=completition_time.strftime("%Y-%m-%d %H:%M")
		except:
			val['completion_time']='NA'
		val['file_size']=f"{file_size} MB"
		datadump.append(val)
	resp = Response(response=json.dumps(datadump), status=200,  mimetype="application/json")
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp

if __name__ == '__main__':
	app.run(host='0.0.0.0')