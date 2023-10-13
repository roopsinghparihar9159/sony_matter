from conf import *
import logging
from subprocess import PIPE,Popen
import re
from flask import Flask, request

app = Flask(__name__)

logging.basicConfig(filename="api-log.log",
		format='%(asctime)s %(message)s',
		filemode='a+')
logger = logging.getLogger()

@app.route("/ctrl",methods=['POST','GET'])
def ctrl(environ,start_response):      #Listen to SNS webhook json and insert the required information in database
		logger.setLevel(logging.DEBUG)
		status = '200 OK'
		response_body=b"status ok"
		response_headers = [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', "*")]
		start_response(status,response_headers)
		fields=request.parse_formvars(environ)
		ch=fields.get('ch')
		action=fields.get('action')
		content_id=fields.get('content_id')
		content_title=fields.get('content_title')
		content_title = re.sub('[^a-zA-Z0-9 \n\.]', '', content_title)
		content_title=content_title.replace(' ','_')
		if(action == "start"):
			logger.info(f"PTI{ch} started")
			cmd=f"/bin/Capture -n 4 -m -1 -d {ch} 2>&1| tail -n -1"
			p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
			out,err=p.communicate()
			if('No input' in out.decode('utf-8')):
				response_body=b"noinput"
				return(response_body)
			cmd0=f"/bin/bash /root/master_start.sh {ch} {content_id} {content_title}"
		elif(action == "stop"):
			logger.info(f"PTI{ch} stopped")
			#response_body="{'content_id':%s,'content_title':%s}" % (content_id,content_title)
			#response_body=response_body.encode('utf-8')
			cmd=f"tmux send-keys -t PTI{ch} 'q' C-m"
			p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True,close_fds=True)
			p.wait()
			cmd0=f"tmux kill-session -t PTI{ch}"
			"""cmd_del=f"rm -f /usr/local/nginx/html/HLS/PTI{ch}/*"
			print(cmd_del)
			p=Popen(cmd_del,stdout=PIPE,stderr=PIPE,shell=True)
			out,err=p.communicate()
			print(out,err)
			cmd_invalidate=f"aws cloudfront create-invalidation --distribution-id E1VSEF43D2WY09 --paths \"/HLS/PTI{ch}/*\" --output json"
			p=Popen(cmd_invalidate,stdout=PIPE,stderr=PIPE,shell=True)"""
			#p.wait()
		else:
			cmd0=""
			print(environ)
		print(f"cmd:{cmd0}")
		p=Popen(cmd0,stdout=PIPE,stderr=PIPE,shell=True,close_fds=True)
		p.wait()
		return(response_body)

def status(environ,start_response):
		status = '200 OK'
		#response_body=b"status ok"
		response_headers = [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', "*")]
		start_response(status,response_headers)
		cmd0="tmux ls | awk -F':' '{print $1}'"
		p=Popen(cmd0,stdout=PIPE,stderr=PIPE,shell=True)
		out,err=p.communicate()
		if('PTI1' in out.decode('utf-8')):
			pti1='True'
		else:
			pti1='False'
		if('PTI2' in out.decode('utf-8')):
			pti2='True'
		else:
			pti2='False'
		response_body=json.dumps({"pti1":pti1,"pti2":pti2}, indent=4)
		response_body=bytes(response_body, 'utf-8')
		return(response_body)

if __name__=="__main__":
	app.run(host='0.0.0.0',port=82,debug=True)