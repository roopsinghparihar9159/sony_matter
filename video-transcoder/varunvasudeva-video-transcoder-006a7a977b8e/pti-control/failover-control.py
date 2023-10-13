import bjoern
import json
from paste.urlmap import URLMap
from paste import request
from datetime import datetime
import os, sys
from time import sleep
from subprocess import PIPE, Popen
import logging
import re
import requests

logging.basicConfig(filename="api-log.log",
		format='%(asctime)s %(message)s',
		filemode='a+')
logger = logging.getLogger()

def ctrl(environ,start_response):      #Listen to SNS webhook json and insert the required information in database
		logger.setLevel(logging.DEBUG)
		status = '200 OK'
		response_body=b"status ok"
		response_headers = [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', "*")]
		start_response(status,response_headers)
		fields=request.parse_formvars(environ)
		action=fields.get('action')
		if(action == "auto"):
			logger.info(f"Failover check switched to Auto")
			cmd=f"tmux send-keys -t pti-health-check:0.0 C-c"
			p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
			out,err=p.communicate()
			cmd=f"tmux send-keys -t pti-health-check:0.0 './failover.sh' C-m"
			p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
			out,err=p.communicate()
		elif(action == "manual"):
			logger.info(f"Failover check switched to Manual")
			source=fields.get('source')
			cmd=f"tmux send-keys -t pti-health-check:0.0 C-c"
			p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True,close_fds=True)
			p.wait()
			cmd=f"./change-route53.sh {source}"
			p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True,close_fds=True)
			out,err=p.communicate()
			print(out,err)
		return(response_body)

#API Functions
map_app = URLMap({})
map_app['/ctrl'] = ctrl

bjoern.listen(map_app, '0.0.0.0', 88)
while True:
	try:
		bjoern.run()
	except KeyboardInterrupt:
		print("Keyboard Interrupt")
		sys.exit()
	except Exception as e:
		print(e)
		continue