from conf import *
import xml
import xmltodict
import json
from flask import Flask, request, Response,jsonify
import requests
import os
import time
import hashlib
app = Flask(__name__)

url = f"http://{eleIp}"
def create_key(uri):
    epoch=str(int(time.time()+60))
    api_auth_key=hashlib.md5(("%s%s%s%s" % (uri,eleUser,eleKey,epoch)).encode('utf-8')).hexdigest()
    api_auth_key=hashlib.md5(("%s%s" % (eleKey,api_auth_key)).encode('utf-8')).hexdigest()
    return(api_auth_key,epoch)

def auth_function(uri):
    api_auth_key,epoch=create_key(uri)
    print(api_auth_key,epoch)
    # url_path=f"{url}{uri}"
    # print(url_path)
    header={"Accept":"application/xml","Content-type":"application/xml","X-Auth-User":eleUser,"X-Auth-Expires":epoch,"X-Auth-Key":api_auth_key}
    return header

@app.route("/test/", methods = ['POST', 'GET'])
def test():
    uri = '/live_events/345/status'
    # api_auth_key,epoch=create_key(uri)
    # print(api_auth_key,epoch)
    url_path=f"{url}{uri}"
    # print(url_path)
    # header={"Accept":"application/xml","Content-type":"application/xml","X-Auth-User":eleUser,"X-Auth-Expires":epoch,"X-Auth-Key":api_auth_key}
    header = auth_function(uri)
    r=requests.get(url_path, headers=header)
    
    result = r.text
    print(result)
    eleData=xmltodict.parse(result)
    # print('eleData',eleData)
    streamStatus=eleData['live_event']['status']
    print(streamStatus)
    return jsonify({'data': f"Api Running Successfully....{streamStatus}"})




# @app.route("/start_and_stop", methods = ['POST', 'GET'])
# def start_and_stop():
#     if request.method == 'POST':
#         id = request.form['id']
#         action = request.form['action']
#         uri = f'/live_events/{id}/{action}'
#         url_path=f"{url}{uri}"
#         header = auth_function(uri)
#         r=requests.post(url_path, headers=header)
#         result = r.text
#         eleData=xmltodict.parse(result)
#         streamStatus=eleData['live_event']['status']
#         return jsonify({'data': f"Api Running Successfully....{streamStatus}"})

def get_request(uri,url):
    header = auth_function(uri)
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
    # streamStatus=eleData['live_event']['status']
    streamStatus = '200 OK'
    return streamStatus

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


@app.route("/status/<id>/", methods = ['GET'])
def get_status(id):
    if request.method == 'GET':
        uri = f'/live_events/{id}/status'
        url_path=f"{url}{uri}"
        url_path_post=f"{url}{uri}"
        status = get_request(uri,url_path)
        return jsonify({'msg': f"Event status:{status} of {id}"})
    return jsonify({'msg': f"Something weng wrong"})

@app.route("/get_all_event_id", methods = ['GET'])
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
def start_and_stop():
    if request.method == 'POST':
        id = request.form['id']
        action = request.form['action']
        uri = f'/live_events/{id}/status'
        url_path=f"{url}{uri}"
        status = get_request(uri,url_path)
        if status == 'complete':
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

@app.route("/create_event", methods = ['POST', 'GET'])
def create_event():
    if request.method == 'POST':
        uri = '/live_events'
        url_path=f"{url}{uri}"
        header = auth_function(uri)
        path = os.getcwd()
        data = f'{path}/live_event_341_c.xml'
        with open(data) as f:
            contents = f.read()
        r=requests.post(url_path, headers=header,data=contents)
        result = r.text
        eleData=xmltodict.parse(result)
        streamStatus=eleData['live_event']['id']
        print('streamStatus',streamStatus)
        return jsonify({'data': f"Api Running Successfully...."})

@app.route("/delete_event/<id>", methods = ['DELETE','GET'])
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

    
    
if __name__ == '__main__':
    app.run(debug = True)
    