import bjoern
import json
from paste.urlmap import URLMap
from paste import request
import os, sys
from time import sleep
import requests
import sqlite3 as sql
from flask import *

def index(environ,start_response):
    con = sql.connect("employee.db")
    con.row_factory=sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    collection_list=[]
    
    for i in rows:
        data=dict()
        for j in i:
            data={
                'id':i['id'],'name':i['name'],'contact':i['contact'],'address':i['address'],'pincode':i['pincode']
            }
        collection_list.append(data)
    print(collection_list)
    print("1")
    status = "200 OK"
    response_body = "status ok"
    response_headers = [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', "*")]
    print('2')
    readbytes=environ['wsgi.input'].read()
    print('3')
    # readstr = readbytes.decode('utf-8')
    res_bytes = json.dumps(collection_list).encode('utf-8')
    # print('Sad guru seva sangh')
    start_response(status, response_headers)
    result = b'collection_list'
    return (res_bytes)


def pti(environ,start_response):      #Listen to SNS webhook json and insert the required information in database
		status = '200 OK'
		# response_body=b"status ok"
		response_body=b'hello'
		response_headers = [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', "*")]
		readbytes=environ['wsgi.input'].read()
		readstr = readbytes.decode('utf-8')
		print('Sad guru seva sangh')
		start_response(status,response_headers)
		return(response_body)

def status(environ,start_response):      #Listen to SNS webhook json and insert the required information in database
		status = '200 OK'
		response_body=b"status ok"
		response_headers = [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', "*")]
		start_response(status,response_headers)
		return(response_body)


map_app = URLMap({})
map_app['/pti'] = pti
map_app['/status'] = status
map_app['/index'] = index

bjoern.listen(map_app, '127.0.0.1',8000)
while True:
	try:
		bjoern.run()
	except KeyboardInterrupt:
		print("Keyboard Interrupt")
		sys.exit()
	except Exception as e:
		print(e)
		continue