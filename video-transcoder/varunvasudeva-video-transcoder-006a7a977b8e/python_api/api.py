# import time
# import sys
import os
from subprocess import Popen, PIPE
from flask import *
import time

app = Flask('__name__')

# rtmp://127.0.0.1/live/<stream key>
@app.route('/start',methods=["POST"])
def start():
	if request.method=="POST":
		jobid=str(time.time()).split('.')[0]
		streamkey=request.form['streamkey']
		type=request.form['type'] # <custom/fb/youtube>
		publishing_url=request.form['publishing_url']
		session=f"{streamkey}_{jobid}"
		cmd=f"tmux kill-session -t {session}"
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		p.wait()
		cmd=f"tmux new-session -d -s {session}"
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		p.wait()
		input_url=f"rtmp://127.0.0.1/live/{streamkey}"
		cmd_relay=f"ffmpeg -i {input_url} -codec copy -f flv {publishing_url}"
		cmd=f"tmux send-keys -t {session}:0.0 '{cmd_relay}' C-m"
		p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		if(p.returncode == 0):
			status='started'
		else:
			status='err500'
	return jsonify({'streamkey':streamkey,'status':status,'jobid':jobid})

@app.route('/stop',methods=["POST"])
def stop():
	if request.method=="POST": 
		try:
			streamkey=request.form['streamkey']
			type=request.form['type']
			jobid=request.form['jobid']
		except:
			status='err404'
			return jsonify({'streamkey':streamkey,'status':status})
		session=f"{streamkey}_{jobid}"
		if(jobid != ""):
			cmd=f"tmux kill-session -t {session}"
			p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
			p.wait()
			if(p.returncode == 0):
				status='stopped'
			else:
				status='err500'
		else:
			status='err404'
	return jsonify({'streamkey':streamkey,'status':status})

@app.route('/test')
def test():
	return jsonify({'status':"working"})

if __name__=="__main__":
	app.run(host='0.0.0.0',port=7005,debug=True)