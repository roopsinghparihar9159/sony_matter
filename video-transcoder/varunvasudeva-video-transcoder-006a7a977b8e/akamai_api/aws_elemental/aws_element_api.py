from conf import *
import xml
import xmltodict
import xml.dom.minidom
import json
from flask import Flask, request, Response,jsonify
import requests
import os
import time
import hashlib
from flask_cors import CORS, cross_origin
app = Flask(__name__)


cors = CORS(app,resources={r"/": {"origins": ""}})
app.config['CORS_HEADERS'] = 'Content-Type'

url = f"http://{eleIp}"

def create_key(uri):
    epoch=str(int(time.time()+60))
    api_auth_key=hashlib.md5(("%s%s%s%s" % (uri,eleUser,eleKey,epoch)).encode('utf-8')).hexdigest()
    api_auth_key=hashlib.md5(("%s%s" % (eleKey,api_auth_key)).encode('utf-8')).hexdigest()
    return(api_auth_key,epoch)

def auth_function(uri):
    api_auth_key,epoch=create_key(uri)
    header={"Accept":"application/xml","Content-type":"application/xml","X-Auth-User":eleUser,"X-Auth-Expires":epoch,"X-Auth-Key":api_auth_key}
    return header

def get_event_list():
    uri = f'/live_events'
    url_path=f"{url}{uri}"
    header = auth_function(uri)
    r=requests.get(url_path, headers=header)
    result = r.text
    list_event = []
    eleData=xmltodict.parse(result)
    for ele in eleData['live_event_list']['live_event']:
        id=ele['@href'].split('/')[-1]
        list_event.append(id)
    return list_event


def get_request(uri,url):
    header = auth_function(uri)
    id = url.split('/')[4]
    get_id = get_event_list()
    if id not in get_id:
        return None
    else: 
        r=requests.get(url, headers=header)
        result = r.text
        eleData=xmltodict.parse(result)
        streamStatus=eleData['live_event']['status']
    return streamStatus

def post_request(uri,path):
    header = auth_function(uri)
    r=requests.post(path, headers=header)
    result = r.text
    eleData=xmltodict.parse(result)
    streamStatus = '200 OK'
    return streamStatus



@app.route("/status/<id>/", methods = ['GET'])
@cross_origin()
def get_status(id):
    if request.method == 'GET':
        uri = f'/live_events/{id}/status'
        url_path=f"{url}{uri}"
        url_path_post=f"{url}{uri}"
        status = get_request(uri,url_path)
        if status:
            return jsonify({'msg': f"Event status:{status} of {id}"})
        else:
            return jsonify({'msg': f"Event Id :{id} not found"})
    return jsonify({'msg': f"Something weng wrong"})

@app.route("/get_all_event_id", methods = ['GET'])
@cross_origin()
def get_all_events():
    if request.method == 'GET':
        uri = f'/live_events'
        url_path=f"{url}{uri}"
        header = auth_function(uri)
        r=requests.get(url_path, headers=header)
        result = r.text
        list_event = []
        eleData=xmltodict.parse(result)
        for ele in eleData['live_event_list']['live_event']:
            event_dict = {}
            result = f"Id:{ele['@href']},----,Name:{ele['name']}"
            print(result)
            id = ele['@href'].split('/')[-1]
            print(id)
            event_dict['id']=ele['@href'].split('/')[-1]
            event_dict['name']=ele['name']
            list_event.append(event_dict)
        data = list_event
        return jsonify({'status_code': "200 OK ",'data':data})
    return jsonify({'msg': f"Something weng wrong"})


@app.route("/start_and_stop", methods = ['POST', 'GET'])
@cross_origin()
def start_and_stop():
    if request.method == 'POST':
        id = request.form['id']
        action = request.form['action']
        uri = f'/live_events/{id}/status'
        url_path=f"{url}{uri}"
        status = get_request(uri,url_path)
        get_id = get_event_list()
        if id not in get_id:
            return jsonify({'msg':f'This event id:{id} not found..Please check it'})
        elif status == 'complete':
            if action == 'reset':
                uri = f'/live_events/{id}/{action}'
                url_path_post=f"{url}{uri}"
                status_code = post_request(uri,url_path_post)
                return jsonify({'data': f"Event Reset Successfully....{status_code}"})
            else:
                msg = f"Please reset event first then {action} event,right now in {status} mode"
                return jsonify({'data': msg})
        elif status == 'pending':
            if action == 'start':
                uri = f'/live_events/{id}/{action}'
                url_path_post=f"{url}{uri}"
                status_code = post_request(uri,url_path_post)
                return jsonify({'data': f"Event Running Successfully....{status_code}"})
            else:
                msg = f"Please start event first,you con't {action} event,right now in {status} mode"
                return jsonify({'data': msg})
        elif status == 'running':
            if action == 'stop':
                uri = f'/live_events/{id}/{action}'
                url_path_post=f"{url}{uri}"
                status_code = post_request(uri,url_path_post)
                return jsonify({'data': f"Event Stop Successfully....{status_code}"})
            else:
                msg = f"Please stop event first then {action} event,right now in {status} mode"
                return jsonify({'data': msg})
        elif status == 'preprocessing':
            if action == 'stop':
                uri = f'/live_events/{id}/{action}'
                url_path_post=f"{url}{uri}"
                status_code = post_request(uri,url_path_post)
                return jsonify({'data': f"Event Stop Successfully....{status_code}"})
            else:
                msg = f"Please stop event first then {action} event,right now in {status} mode"
                return jsonify({'data': msg})
        else:
            if status == 'cancelled':
                if action == 'reset':
                    uri = f'/live_events/{id}/{action}'
                    url_path_post=f"{url}{uri}"
                    status_code = post_request(uri,url_path_post)
                    return jsonify({'msg': f"Event Reset Successfully....",'status_code':status_code})
            else:
                msg = f"Please reset event first then {action} event,right now in {status} mode"
                return jsonify({'data': msg})
    return jsonify({'data': f"Something went wrong"})

def replace_key(key_pra):
   domtree = xml.dom.minidom.parse('live_event_341.xml')
   live_event = domtree.documentElement
#    name_tag = live_event.getElementsByTagName('name')
   network_input = live_event.getElementsByTagName('network_input')
   output_group = live_event.getElementsByTagName('output_group')
#    name = live_event.getElementsByTagName('name')[0].childNodes[0].nodeValue
   uri = network_input[0].getElementsByTagName('uri')[0].childNodes[0].nodeValue
   output_uri = output_group[0].getElementsByTagName('uri')[0].childNodes[0].nodeValue
   output_uri1 = output_group[1].getElementsByTagName('uri')[0].childNodes[0].nodeValue

#    live_event.getElementsByTagName('name')[0].childNodes[0].nodeValue = name_pra

#    start fetching uri of network_input
# rtmp://173.16.16.24/live/Roopsibnbghgugkhih
   split_uri = uri.rsplit('/',1)
   uri_index_one = split_uri[1]
   uri_index_one = key_pra
   end_point_uri = uri_index_one
   uri_assign = f"{split_uri[0]}/{end_point_uri}"
   network_input[0].getElementsByTagName('uri')[0].childNodes[0].nodeValue = uri_assign

   #    output uri fetch
#    http://p-ep2101752.i.akamaientrypoint.net/2101752/outputkeyassign/master

   split_output_uri = output_uri.rsplit('/',2)
   ouput_uri_key = split_output_uri[-2]
   ouput_uri_key = key_pra
   output_key_assign = f"{split_output_uri[0]}/{ouput_uri_key}/{split_output_uri[2]}"
   output_group[0].getElementsByTagName('uri')[0].childNodes[0].nodeValue = output_key_assign


   #output_uri_fetch 2
#    /data/mnt/storage/FTP/PW/$d$/keychabge-$t$
   split_output_uri1 = output_uri1.rsplit('/',1)
   split_output_uri1_key = split_output_uri1[1].split('-')
   split_output_uri1_key_get = split_output_uri1_key[0]
   split_output_uri1_key_get = key_pra
   output_1_uri = f"{split_output_uri1[0]}/{split_output_uri1_key_get}-{split_output_uri1_key[1]}"
   output_group[1].getElementsByTagName('uri')[0].childNodes[0].nodeValue = output_1_uri


   domtree.writexml(open('live_event_341.xml','w'))
#    with open('live_event_341.xml') as file:
#     result = file.read()
   return f"Change key Successfully..."

def xml_file_reading(name_pra,key_pra):
   domtree = xml.dom.minidom.parse('live_event_341.xml')
   live_event = domtree.documentElement
   name_tag = live_event.getElementsByTagName('name')
   network_input = live_event.getElementsByTagName('network_input')
   output_group = live_event.getElementsByTagName('output_group')
   name = live_event.getElementsByTagName('name')[0].childNodes[0].nodeValue
   uri = network_input[0].getElementsByTagName('uri')[0].childNodes[0].nodeValue
   output_uri = output_group[0].getElementsByTagName('uri')[0].childNodes[0].nodeValue
   output_uri1 = output_group[1].getElementsByTagName('uri')[0].childNodes[0].nodeValue

   live_event.getElementsByTagName('name')[0].childNodes[0].nodeValue = name_pra

#    start fetching uri of network_input
# rtmp://173.16.16.24/live/Roopsibnbghgugkhih
   split_uri = uri.rsplit('/',1)
   uri_index_one = split_uri[1]
   uri_index_one = key_pra
   end_point_uri = uri_index_one
   uri_assign = f"{split_uri[0]}/{end_point_uri}"
   network_input[0].getElementsByTagName('uri')[0].childNodes[0].nodeValue = uri_assign

   #    output uri fetch
#    http://p-ep2101752.i.akamaientrypoint.net/2101752/outputkeyassign/master

   split_output_uri = output_uri.rsplit('/',2)
   ouput_uri_key = split_output_uri[-2]
   ouput_uri_key = key_pra
   output_key_assign = f"{split_output_uri[0]}/{ouput_uri_key}/{split_output_uri[2]}"
   output_group[0].getElementsByTagName('uri')[0].childNodes[0].nodeValue = output_key_assign


   #output_uri_fetch 2
#    /data/mnt/storage/FTP/PW/$d$/keychabge-$t$
   split_output_uri1 = output_uri1.rsplit('/',1)
   split_output_uri1_key = split_output_uri1[1].split('-')
   split_output_uri1_key_get = split_output_uri1_key[0]
   split_output_uri1_key_get = key_pra
   output_1_uri = f"{split_output_uri1[0]}/{split_output_uri1_key_get}-{split_output_uri1_key[1]}"
   output_group[1].getElementsByTagName('uri')[0].childNodes[0].nodeValue = output_1_uri


   domtree.writexml(open('live_event_341.xml','w'))
   with open('live_event_341.xml') as file:
    result = file.read()
   return result

@app.route("/replace_key_event", methods = ['POST', 'GET'])
@cross_origin()
def replace_key_event():
    if request.method == 'POST':
        # name = request.form['name']
        key = request.form['key']

        # uri = '/live_events'
        # url_path=f"{url}{uri}"
        # header = auth_function(uri)
        
        contents = replace_key(key)
        # requests.post(url_path, headers=header,data=contents)
        # result = r.text
        # eleData=xmltodict.parse(result)
        # job_id=eleData['live_event']['id']
        # print('streamStatus',streamStatus)
        print('contents',contents)
        return jsonify({'msg': f"Change key Successfully...."})
    return jsonify({'msg': f"Something went wrong...."})




@app.route("/create_event", methods = ['POST', 'GET'])
@cross_origin()
def create_event():
    if request.method == 'POST':
        name = request.form['name']
        key = request.form['key']

        uri = '/live_events'
        url_path=f"{url}{uri}"
        header = auth_function(uri)
        
        contents = xml_file_reading(name,key)
        r=requests.post(url_path, headers=header,data=contents)
        result = r.text
        eleData=xmltodict.parse(result)
        job_id=eleData['live_event']['id']
        # print('streamStatus',streamStatus)
        return jsonify({'msg': f"Event created Successfully....",'JOB_ID':job_id})
    return jsonify({'msg': f"Something went wrong...."})

@app.route("/delete_event/<id>", methods = ['DELETE','GET'])
@cross_origin()
def delete_event(id):
    if request.method == 'DELETE':
        uri = f'/live_events/{id}'
        url_path=f"{url}{uri}"
        header = auth_function(uri)
        get_id = get_event_list()
        if id not in get_id:
            return jsonify({'status_code':'404 NotFound'})
        else:
            requests.delete(url_path, headers=header)
            return jsonify({'msg': f"Event Deleted Successfully...."})
    return jsonify({'msg': f"Something went wrong...."})
    

@app.route("/cancel_event/<id>", methods = ['POST','GET'])
@cross_origin()
def cancel_event(id):
    if request.method == 'POST':
        uri = f'/live_events/{id}'
        url_path=f"{url}{uri}"
        get_id = get_event_list()
        status = get_request(uri,url_path)
        if id not in get_id:
            return jsonify({'msg': f"You can't cancelled this event id,because not found",'status_code':'404 NotFound'})
        elif status == 'cancelled':
            return jsonify({'msg': f"This event id:{id} is already cancelled."})
        else:
            uri = f'/live_events/{id}/cancel'
            # http://server_ip/live_events/15/cancel
            url_path=f"{url}{uri}"
            response = post_request(uri,url_path)
            return jsonify({'status_code': response})
    return jsonify({'msg': f"Somthing went wrong..."})

@app.route("/update_event", methods = ['PUT','GET'])
@cross_origin()
def update_event():
    if request.method == 'PUT':
        id = request.form['id']
        name = request.form['name']

        uri = f'/live_events/{id}'
        url_path=f"{url}{uri}"
        get_id = get_event_list()
        status = get_request(uri,url_path)
        if id not in get_id:
            return jsonify({'msg': f"You can't update this event id,because not found",'status_code':'404 NotFound'})
        elif status == 'running':
            return jsonify({'msg': f"This event id:{id} can't updated because right now running event."})
        else:
            uri = f'/live_events/{id}'
            url_path=f"{url}{uri}"
            header = auth_function(uri)
            content = f"<live_event><id>{id}</id><name>{name}</name></live_event>"
            r=requests.put(url_path, headers=header,data=content)
            result = r.text
            eleData=xmltodict.parse(result)
            streamStatus = '200 OK'
            return jsonify({'msg': 'Event updated Sucessfully..','status_code':streamStatus})
    return jsonify({'msg': f"Somthing went wrong..."})

    
    
if __name__ == '__main__':
    app.run(debug = True)
    