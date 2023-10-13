from datetime import datetime,date
from datetime import timedelta

from flask import Flask,jsonify,request
from flask_cors import CORS,cross_origin  
import requests
from akamai.edgegrid import EdgeGridAuth
from urllib.parse import urljoin

from conf import *


app = Flask(__name__)

import mysql_api

cors = CORS(app,resources={r"/": {"origins": ""}})
app.config['CORS_HEADERS'] = 'Content-Type'

endpoint = "identity-management/v3/user-admin/groups/"  #get a groups

# endpoint = "datastream-config-api/v2/log/groups/{groupId}/properties"
 

headers = {"Accept": "application/json"}


@app.route('/get_group_list',methods=["GET"])
@cross_origin()
def get_group_list():
    # url=http://127.0.0.1:5000/get_group_list
    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        querystring = {
        "actions": True
        } 
        result = s.get(urljoin(baseurl, endpoint),headers=headers,params=querystring)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/get_group_by_id/<groupId>', methods=['GET'])
@cross_origin()
def get_group_details_by_id(groupId):
    endpoint = f"identity-management/v3/user-admin/groups/{groupId}"
    # url=http://127.0.0.1:5000/get_group_by_id/233179
    
    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        
        result = s.get(urljoin(baseurl, endpoint),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/get_property_of_group_by_id/<groupId>',methods=['GET'])
@cross_origin()
def get_property_of_group(groupId):
    # groupId=230985
    # propertyId = 11122159
    # ur=http://127.0.0.1:5000/get_property_of_group_by_id/231754
    path = '/identity-management/v3/user-admin/properties'
    
    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        querystring = {
            "groupId": groupId
        } 
        result = s.get(urljoin(baseurl, path),headers=headers,params=querystring)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/get_all_cpcode',methods=['GET'])
@cross_origin()
def get_all_cpcode():
    # url=http://127.0.0.1:5000/get_all_cpcode
    path = "/cprg/v1/cpcodes"
    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/get_cpcode/<cpcodeId>',methods=['GET'])
@cross_origin()
def get_cpcode(cpcodeId):
    path = f"/cprg/v1/cpcodes/{cpcodeId}"
    # url=http://127.0.0.1:5000/get_cpcode/1414754
    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)
        
@app.route('/get_adaptive_media_delivery_historical_data',methods=['GET'])
@cross_origin()
def get_adaptive_media_delivery_historical_data():
    day_no = int(request.args.get('days'))
    current_date = datetime.now()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    metrics  = request.args.get('metrics')
    cpcodes = request.args.get('cpcodes') 
    dimensions = request.args.get('dimensions')
    # url = http://127.0.0.1:5000/get_adaptive_media_delivery_historical_data?&cpcodes=1456363,1456910&dimensions=1,&metrics=107,221,7,455,9,12&days=30
    path = f"/media-delivery-reports/v1/adaptive-media-delivery/data?startDate={start_date}&endDate={end_date}&cpcodes={cpcodes}&ipVersion=ipv4&limit=1000&offset=0&deliveryOption=http&deliveryFormat=hls&deliveryType=On demand&dimensions={dimensions},&metrics={metrics}"

    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
    
    return jsonify(data)

@app.route('/get_adaptive_media_delivery_realtime_data',methods=['GET'])
@cross_origin()
def get_adaptive_media_delivery_realtime_data():
    current_date = datetime.now()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=2)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    metrics  = request.args.get('metrics')
    cpcodes = request.args.get('cpcodes') 
    dimensions = request.args.get('dimensions')
    # url_hit=http://127.0.0.1:5000/get_adaptive_media_delivery_realtime_data?&cpcodes=1456363,1450392,1456910&dimensions=&metrics=622,616,617,618,619,620,621
    path = f"/media-delivery-reports/v1/adaptive-media-delivery/realtime-data?startDate={start_date}&endDate={end_date}&cpcodes={cpcodes}&dimensions={dimensions}&metrics={metrics}&limit=300&offset=0&aggregation=86400&enableCPCodeName=True"

    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
    
    return jsonify(data)

@app.route('/hits_by_os',methods=['GET'])
@cross_origin()
def hits_by_os():
    day_no = request.args.get('days',1,type=int)
    ObjectIds = request.args.get('ObjectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    count = 0
    res = {}
    while count<=5:
        path = f"/reporting-api/v1/reports/hits-by-os/versions/1/report-data?start={start_date}&end={end_date}&objectIds={ObjectIds}&metrics=successfulHits,successfulHitsPercent&dataWrapNumberOfItems=9&dataWrapLabel=Other"
        # http://127.0.0.1:5000/hits_by_os?days=20&ObjectIds=1456363
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            json_data = result.json()
            try:
                res['data'] = json_data['data']                
                if res['data']:
                    break
            except Exception:
                res['data']=json_data
        count += 1
    data = {
        "result":res,
        "status_code":result.status_code
    }
    return jsonify(data)


@app.route('/hits_by_time',methods=['GET'])
@cross_origin()
def hits_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/hits_by_time?days=17&objectIds=1456363
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/hits-by-time/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&interval=HOUR&metrics=edgeHitsPerSecond,edgeHitsPerSecondMax,edgeHitsPerSecondMin,edgeHitsSlope,edgeHitsTotal,hitsOffload,hitsOffloadAvg,hitsOffloadMax,hitsOffloadMin,hitsOffloadSlope,originHitsPerSecond,originHitsPerSecondMax,originHitsPerSecondMin,originHitsSlope,originHitsTotal"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            json_data = result.json()
            res = {}
            res['data']=json_data['data']
            data = {
                "result":res,
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg="CPCode is Required..."
        return jsonify({"msg":msg})

@app.route('/hits_by_cpcode',methods=['GET'])
@cross_origin()
def hits_by_cpcode():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/hits_by_cpcode?days=17&objectIds=1456363
    if objectIds is not None:
        path=f"/reporting-api/v1/reports/hits-by-cpcode/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeHits,hitsOffload,originHits&filters=delivery_type=secure,ip_version=ipv4,ip_version=ipv6"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            json_data = result.json()
            res = {}
            res['data'] = json_data['data']
            data = {
                "result":res,
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg="CPCode is Required..."
        return jsonify({"msg":msg})

@app.route('/hits_by_ip',methods=['GET'])        
@cross_origin()
def hits_by_ip():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/hits_by_ip?days=17&objectIds=1456363
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/hits-by-ip/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=successfulHits"
        
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            json_data = result.json()
            res = {}
            res['data'] = json_data['data']
            data = {
                "result":res,
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg="CPCode is Required..."
        return jsonify({"msg":msg})

@app.route('/bytes_by_httpversion',methods=['GET'])        
@cross_origin()
def bytes_by_httpversion():
    day_no = int(request.args.get('days'))
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/bytes_by_httpversion?days=17&objectIds=1456363
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/bytes-by-httpversion/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeBytes,edgeBytesPercent"
        
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            json_data = result.json()
            res = {}
            res['data'] = json_data['data']
            data = {
                "result":res,
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg="CPCode is Required..."
        return jsonify({"msg":msg})

@app.route('/apivolume_by_owner',methods=['GET'])        
@cross_origin()
def apivolume_by_owner():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/apivolume_by_owner?days=17
    path = f"/reporting-api/v1/reports/apivolume-by-owner/versions/1/report-data?start={start_date}&end={end_date}&allObjectIds=True&metrics=bytesPercent,bytesTotal"
    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/apirequests_by_agentfamily',methods=['GET'])        
@cross_origin()
def apirequests_by_agentfamily():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/apirequests_by_agentfamily?days=17
    path = f"/reporting-api/v1/reports/apirequests-by-agentfamily/versions/1/report-data?start={start_date}&end={end_date}&allObjectIds=True&metrics=requestsPercent,requestsTotal"

    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/apirequests_by_endpoint',methods=['GET'])        
@cross_origin()
def apirequests_by_endpoint():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/apirequests_by_endpoint?days=17
    path = f"/reporting-api/v1/reports/apirequests-by-endpoint/versions/1/report-data?start={start_date}&end={end_date}&allObjectIds=True&metrics=requestsPercent%2CrequestsTotal"

    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/apirequests_by_httpmethod',methods=['GET'])        
@cross_origin()
def apirequests_by_httpmethod():
    day_no = request.args.get('days',1,type=int)    
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/apirequests_by_httpmethod?days=17
    path = f"/reporting-api/v1/reports/apirequests-by-httpmethod/versions/1/report-data?start={start_date}&end={end_date}&allObjectIds=True&metrics=requestsPercent,requestsTotal"
    
    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/apirequests_by_owner',methods=['GET'])        
@cross_origin()
def apirequests_by_owner():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/apirequests_by_owner?days=17
    path = f"/reporting-api/v1/reports/apirequests-by-owner/versions/1/report-data?start={start_date}&end={end_date}&allObjectIds=True&metrics=requestsPercent,requestsTotal"


    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/apiusage_by_time',methods=['GET'])        
@cross_origin()
def apiusage_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/apiusage_by_time?days=17
    path = f"/reporting-api/v1/reports/apiusage-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=HOUR&allObjectIds=True&metrics=bytes,bytesTotal"


    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/apiusagedetails_by_time',methods=['GET'])        
@cross_origin()
def apiusagedetails_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/apiusagedetails_by_time?&days=18
    path = f"/reporting-api/v1/reports/apiusagedetails-by-time/versions/1/report-data?start={start_date}&end={end_date}&allObjectIds=True&metrics=clientId,clientIp"


    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/apivolume_by_agentfamily',methods=['GET'])        
@cross_origin()
def apivolume_by_agentfamily():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/apivolume_by_agentfamily?&days=18
    path = f"/reporting-api/v1/reports/apivolume-by-agentfamily/versions/1/report-data?start={start_date}&end={end_date}&allObjectIds=True&metrics=bytesPercent,bytesTotal"

    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/bytes_by_cpcode',methods=['GET'])        
@cross_origin()
def bytes_by_cpcode():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/bytes_by_cpcode?&days=18&objectIds=1349555
    
    path = f"/reporting-api/v1/reports/bytes-by-cpcode/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeBytes"
    
    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        res = result.json()
        data = {
            "result":res['data'],
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/bytes_by_timeandhttpversion',methods=['GET'])        
@cross_origin()
def bytes_by_timeandhttpversion():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/bytes_by_timeandhttpversion?&days=18&objectIds=1349555
    path = f"/reporting-api/v1/reports/bytes-by-timeandhttpversion/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeBitsPerSecond"
    
    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/bytes_by_tophostnameandtime',methods=['GET'])        
@cross_origin()
def bytes_by_tophostnameandtime():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/bytes_by_tophostnameandtime?&days=18&objectIds=1349555
    path = f"/reporting-api/v1/reports/bytes-by-tophostnameandtime/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=maxEdgeBytes"
    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/carbondata_by_time',methods=['GET'])        
@cross_origin()
def carbondata_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/carbondata_by_time?&days=18&objectIds=1349555

    path = f"/reporting-api/v1/reports/carbondata-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=DAY&objectIds={objectIds}&metrics=edgeBytesTotal,calculatedEmissionsGrams&filters=delivery_type=secure"

    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/carbondata_by_servergeo',methods=['GET'])        
@cross_origin()
def carbondata_by_servergeo():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/carbondata_by_servergeo?days=18&objectIds=1349555
    path = f"/reporting-api/v1/reports/carbondata-by-servergeo/versions/1/report-data?start={start_date}&end={end_date}&interval=DAY&objectIds={objectIds}&metrics=calculatedEmissionsGrams,edgeBytes"

    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/duv_by_browser',methods=['GET'])        
@cross_origin()
def duv_by_browser():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/duv_by_browser?days=18&objectIds=1349555
    path = f"/reporting-api/v1/reports/duv-by-browser/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=uniqueVisitorsMax,uniqueVisitorsPercent&dataWrapNumberOfItems=9&dataWrapLabel=Other"
    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/uv_by_country',methods=['GET'])        
@cross_origin()
def uv_by_country():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/uv_by_country?days=19&objectIds=1349555
    path = f"/reporting-api/v1/reports/duv-by-country/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=uniqueVisitorsCountry,uniqueVisitorsMax"

    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/duv_by_os',methods=['GET'])        
@cross_origin()
def duv_by_os():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/duv_by_os?days=19&objectIds=1349555
    path = f"/reporting-api/v1/reports/duv-by-os/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=uniqueVisitorsMax,uniqueVisitorsPercent&dataWrapNumberOfItems=9&dataWrapLabel=Other"

    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/duv_by_province',methods=['GET'])        
@cross_origin()
def duv_by_province():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/duv_by_province?days=19&objectIds=1349555
    path = f"/reporting-api/v1/reports/duv-by-province/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=uniqueVisitorsMax,uniqueVisitorsProvince"

    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/duv_by_state',methods=['GET'])        
@cross_origin()
def duv_by_state():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/duv_by_state?days=19&objectIds=1349555
    count = 0
    res = {}
    while count<=5:
        path = f"/reporting-api/v1/reports/duv-by-state/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=uniqueVisitorsMax,uniqueVisitorsState"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            json_data = result.json()
            try:
                res['data'] = json_data['data']                
                if res['data']:
                    break
            except Exception:
                res['data']=json_data
            count += 1
    data = {
        "result":res,
        "status_code":result.status_code
    }
    return jsonify(data)

@app.route('/duv_by_time',methods=['GET'])        
@cross_origin()
def duv_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/duv_by_time?days=19&objectIds=1349555
    path = f"/reporting-api/v1/reports/duv-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=DAY&objectIds={objectIds}&metrics=allUniqueVisitors,allUniqueVisitorsAverage"
    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)

@app.route('/ecresponse_by_time',methods=['GET'])        
@cross_origin()
def ecresponse_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/ecresponse_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/ecresponse-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeRequests0xxPerSecond,edgeRequests1xxPerSecond"    
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/ectraffic_by_time',methods=['GET'])        
@cross_origin()
def ectraffic_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/ectraffic_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/ectraffic-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeBitsPerSecond,edgeBitsPerSecondMax"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/endpoint_api_key_usage_by_time',methods=['GET'])        
@cross_origin()
def endpoint_api_key_usage_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/endpoint_api_key_usage_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/endpoint-api-key-usage-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeBytes,edgeBytesMax"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/endpoint_errors_by_response_class',methods=['GET'])        
@cross_origin()
def endpoint_errors_by_response_class():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/endpoint_errors_by_response_class?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/endpoint-errors-by-response-class/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeHits,edgeHitsMax&filters=api_key=577595,api_key=577597,endpoint_id=577597,endpoint_id=577596"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/endpoint_errors_by_response_code',methods=['GET'])        
@cross_origin()
def endpoint_errors_by_response_code():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/endpoint_errors_by_response_code?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/endpoint-errors-by-response-code/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeHits,edgeHitsMax&filters=api_key=577598,api_key=577596,endpoint_id=577599,endpoint_id=577596"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/endpoint_errors_by_time',methods=['GET'])        
@cross_origin()
def endpoint_errors_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/endpoint_errors_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/endpoint-errors-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeHits,edgeHitsMax&filters=api_key=577598,api_key=577595,endpoint_id=577596,endpoint_id=577597"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/endpoint_hits_by_apikey',methods=['GET'])        
@cross_origin()
def endpoint_hits_by_apikey():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/endpoint_hits_by_apikey?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/endpoint-hits-by-apikey/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeBytes,edgeBytesMax"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/endpoint_hits_by_method_and_response',methods=['GET'])        
@cross_origin()
def endpoint_hits_by_method_and_response():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/endpoint_hits_by_method_and_response?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/endpoint-hits-by-method-and-response/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeBytes%2CedgeBytesMax"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/endpoint_usage_by_method',methods=['GET'])        
@cross_origin()
def endpoint_usage_by_method():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/endpoint_usage_by_method?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/endpoint-usage-by-method/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeBytes,edgeBytesMax&filters=endpoint_id=577596,endpoint_id=577597,http_method=put,http_method=get"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/endpoint_usage_by_response_code',methods=['GET'])        
@cross_origin()
def endpoint_usage_by_response_code():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/endpoint_usage_by_response_code?days=19&objectIds=1349555
    if objectIds is not None:
        path =f"/reporting-api/v1/reports/endpoint-usage-by-response-code/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeBytes,edgeBytesMax&filters=endpoint_id=577596,endpoint_id=577597,http_method=put,http_method=get"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/endpoint_usage_by_time',methods=['GET'])        
@cross_origin()
def endpoint_usage_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/endpoint_usage_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path =f"/reporting-api/v1/reports/endpoint-usage-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeBytes,edgeBytesMax&filters=endpoint_id=577596,endpoint_id=577595,http_method=get,http_method=put"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/enhancedtraffic_by_country',methods=['GET'])        
@cross_origin()
def enhancedtraffic_by_country():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/enhancedtraffic_by_country?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/enhancedtraffic-by-country/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=country,edgeBytes"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/enhancedtraffic_by_province',methods=['GET'])        
@cross_origin()
def enhancedtraffic_by_province():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/enhancedtraffic_by_province?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/enhancedtraffic-by-province/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeBytes,edgeHits&filters=delivery_type=secure"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/enhancedtraffic_by_state',methods=['GET'])        
@cross_origin()
def enhancedtraffic_by_state():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/enhancedtraffic_by_state?&days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/enhancedtraffic-by-state/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeBytes,edgeHits,state&filters=delivery_type=secure"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/estimatedecresponse_by_time',methods=['GET'])        
@cross_origin()
def estimatedecresponse_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/estimatedecresponse_by_time?days=2&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/estimatedecresponse-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeRequests0xxPerSecond%2CedgeRequests1xxPerSecond,edgeRequests2xxPerSecond,edgeRequests3xxPerSecond,edgeRequests4xxPerSecond,edgeRequests5xxPerSecond,originRequests0xxPerSecond,originRequests1xxPerSecond,originRequests2xxPerSecond,originRequests3xxPerSecond,originRequests4xxPerSecond,originRequests5xxPerSecond"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/estimatedectraffic_by_time',methods=['GET'])        
@cross_origin()
def estimatedectraffic_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/estimatedectraffic_by_time?days=2&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/estimatedectraffic-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeBitsPerSecond,edgeBitsPerSecondMax"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})


@app.route('/flashlivetraffic_by_time',methods=['GET'])        
@cross_origin()
def flashlivetraffic_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/flashlivetraffic_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/flashlivetraffic-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeBitsPerSecond,edgeBitsPerSecondMax,viewers,edgeHitsPerSecond,edgeBytesTotal,edgeHitsPerSecondMax,edgeHitsTotal"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/gtm_availability',methods=['GET'])        
@cross_origin()
def gtm_availability():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/gtm_availability?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/gtm-availability/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=avail_pct,avg_avail_pct"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/hits_by_browser',methods=['GET'])        
@cross_origin()
def hits_by_browser():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    res = {}
    count = 0

    while count<=5:
        path = f"/reporting-api/v1/reports/hits-by-browser/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=successfulHits,successfulHitsPercent&dataWrapNumberOfItems=9&dataWrapLabel=Other"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            json_data = result.json()
            try:
                res['data'] = json_data['data']                
                if res['data']:
                    break
            except Exception:
                res['data']=json_data
            count += 1
    data = {
        "result":res,
        "status_code":result.status_code
    }
    return jsonify(data)

@app.route('/hits_by_httpversion',methods=['GET'])        
@cross_origin()
def hits_by_httpversion():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/hits_by_httpversion?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/hits-by-httpversion/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeHits,edgeHitsPercent&filters=ca=cacheable,ca=non_cacheable,delivery_type=secure"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            json_data = result.json()
            res={}
            res['data'] = json_data['data']
            data = {
                "result":res,
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/hits_by_timeandhttpversion',methods=['GET'])        
@cross_origin()
def hits_by_timeandhttpversion():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/hits_by_timeandhttpversion?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/hits-by-timeandhttpversion/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeHitsPerSecond&filters=ca%3Dcacheable%2Cca%3Dnon_cacheable%2Cdelivery_type%3Dsecure"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/hits_by_tophostnameandtime',methods=['GET'])        
@cross_origin()
def hits_by_tophostnameandtime():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/hits_by_tophostnameandtime?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/hits-by-tophostnameandtime/versions/1/report-data?start={start_date}&end={end_date}&interval=HOUR&objectIds={objectIds}&metrics=maxEdgeHits"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            json_data = result.json()
            res = {}
            res['data'] = json_data['data']
            data = {
                "result":res,
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/hostname_bytes_by_cpcode',methods=['GET'])        
@cross_origin()
def hostname_bytes_by_cpcode():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/hostname_bytes_by_cpcode?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/hostname-bytes-by-cpcode/versions/2/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeBytes&filters=ca%3Dcacheable%2Cca%3Dnon_cacheable%2Cdelivery_type%3Dsecure"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})


@app.route('/hostname_bytes_by_hostname',methods=['GET'])        
@cross_origin()
def hostname_bytes_by_hostname():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/hostname_bytes_by_hostname?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/hostname-bytes-by-hostname/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeBytes&filters=ca=cacheable,ca=non_cacheable,delivery_type=secure"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})


@app.route('/hostname_bytes_by_httpversion',methods=['GET'])        
@cross_origin()
def hostname_bytes_by_httpversion():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/hostname_bytes_by_httpversion?days=2&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/hostname-bytes-by-httpversion/versions/2/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeBytes%2CedgeBytesPercent&filters=ca%3Dcacheable%2Cca%3Dnon_cacheable%2Cdelivery_type%3Dsecure"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/hostname_bytes_by_time',methods=['GET'])        
@cross_origin()
def hostname_bytes_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/hostname_bytes_by_time?days=20&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/hostname-bytes-by-time/versions/2/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeBitsPerSecond,edgeBitsPerSecondMax&filters=ca=cacheable,ca=non_cacheable,delivery_type%3Dsecure"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/hostname_bytes_by_timeandhttpversion',methods=['GET'])        
@cross_origin()
def hostname_bytes_by_timeandhttpversion():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/hostname_bytes_by_timeandhttpversion?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/hostname-bytes-by-timeandhttpversion/versions/2/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeBitsPerSecond&filters=ca=cacheable,ca=non_cacheable,delivery_type=secure"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/hostname_hits_by_cpcode',methods=['GET'])        
@cross_origin()
def hostname_hits_by_cpcode():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/hostname_hits_by_cpcode?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/hostname-hits-by-cpcode/versions/2/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeHits&filters=ca=cacheable,ca=non_cacheable,delivery_type=secure"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})
@app.route('/hostname_hits_by_hostname',methods=['GET'])        
@cross_origin()
def hostname_hits_by_hostname():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/hostname_hits_by_hostname?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/hostname-hits-by-hostname/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeHits&filters=ca=cacheable,ca=non_cacheable,delivery_type=secure"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/hostname_hits_by_httpversion',methods=['GET'])        
@cross_origin()
def hostname_hits_by_httpversion():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/hostname_hits_by_httpversion?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/hostname-hits-by-time/versions/2/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeHitsPerSecond,edgeHitsPerSecondMax&filters=ca=cacheable,ca=non_cacheable,delivery_type=secure"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/hostname_hits_by_timeandhttpversion',methods=['GET'])        
@cross_origin()
def hostname_hits_by_timeandhttpversion():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/hostname_hits_by_timeandhttpversion?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/hostname-hits-by-timeandhttpversion/versions/2/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeHitsPerSecond&filters=ca=cacheable,ca=non_cacheable,delivery_type=secure"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/hostname_traffic_by_response',methods=['GET'])        
@cross_origin()
def hostname_traffic_by_response():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/hostname_traffic_by_response?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/hostname-traffic-by-response/versions/2/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeHits,edgeHitsPercent&filters=ca=cacheable,ca=non_cacheable,delivery_type=secure"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})


@app.route('/hostname_traffic_by_responseclass',methods=['GET'])        
@cross_origin()
def hostname_traffic_by_responseclass():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/hostname_traffic_by_responseclass?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/hostname-traffic-by-responseclass/versions/2/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeHits,edgeHitsPercent&filters=ca=cacheable,ca=non_cacheable,delivery_type=secure"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/hostname_traffic_by_timeandresponse',methods=['GET'])        
@cross_origin()
def hostname_traffic_by_timeandresponse():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/hostname_traffic_by_timeandresponse?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/hostname-traffic-by-timeandresponse/versions/2/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeHitsPerSecond&filters=ca=cacheable,ca=non_cacheable,delivery_type=secure"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})


@app.route('/hostname_traffic_by_timeandresponseclass',methods=['GET'])        
@cross_origin()
def hostname_traffic_by_timeandresponseclass():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/hostname_traffic_by_timeandresponseclass?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/hostname-traffic-by-timeandresponseclass/versions/2/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeHitsPerSecond&filters=ca=cacheable,ca=non_cacheable,delivery_type=secure"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/im_traffic_by_image_and_browser',methods=['GET'])        
@cross_origin()
def im_traffic_by_image_and_browser():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/im_traffic_by_image_and_browser?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/im-traffic-by-image-and-browser/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeImageBytes,edgeImageBytesPercent&filters=token_policy=577595,token_policy=577599"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/imbytes_by_browser',methods=['GET'])        
@cross_origin()
def imbytes_by_browser():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/imbytes_by_browser?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/imbytes-by-browser/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeImageBytes,edgeImageBytesPercent&filters=token_policy=577598,token_policy=577599"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/imbytes_by_imagetype',methods=['GET'])        
@cross_origin()
def imbytes_by_imagetype():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/imbytes_by_imagetype?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/imbytes-by-imagetype/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeImageBytes,edgeImageBytesPercent&filters=token_policy=577595,token_policy=577597"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/imbytes_by_policy',methods=['GET'])        
@cross_origin()
def imbytes_by_policy():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/imbytes_by_imagetype?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/imbytes-by-policy/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeImageBytes&filters=token_policy=577598,token_policy=577599"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/imbytes_by_policyandbrowser',methods=['GET'])        
@cross_origin()
def imbytes_by_policyandbrowser():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/imbytes_by_policyandbrowser?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/imbytes-by-policyandbrowser/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeImageBytes&filters=token_policy=577597,token_policy=577599"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/imbytes_by_policyandimagetype',methods=['GET'])        
@cross_origin()
def imbytes_by_policyandimagetype():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/imbytes_by_policyandimagetype?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/imbytes-by-policyandimagetype/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeImageBytes&filters=token_policy=577596,token_policy=577599"
        
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/imbytes_by_policyandwidth',methods=['GET'])        
@cross_origin()
def imbytes_by_policyandwidth():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/imbytes_by_policyandwidth?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/imbytes-by-policyandwidth/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeImageBytes&filters=token_policy=577595,token_policy=577598"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/imbytes_by_width',methods=['GET'])        
@cross_origin()
def imbytes_by_width():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/imbytes_by_width?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/imbytes-by-width/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeImageBytes,edgeImageBytesPercent&filters=token_policy=577595,token_policy=577599"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/imhits_by_browser',methods=['GET'])        
@cross_origin()
def imhits_by_browser():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/imhits_by_browser?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/imhits-by-browser/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeImageHits,edgeImageHitsPercent&filters=token_policy=577598,token_policy=577596"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/imhits_by_imagetype',methods=['GET'])        
@cross_origin()
def imhits_by_imagetype():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/imhits_by_imagetype?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/imhits-by-imagetype/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeImageHits,edgeImageHitsPercent&filters=token_policy=577595,token_policy=577597"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/imhits_by_policy',methods=['GET'])        
@cross_origin()
def imhits_by_policy():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/imhits_by_policy?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/imhits-by-policy/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeImageHits&filters=token_policy=577598,token_policy=577596"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})


@app.route('/imhits_by_policyandbrowser',methods=['GET'])        
@cross_origin()
def imhits_by_policyandbrowser():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/imhits_by_policyandbrowser?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/imhits-by-policyandimagetype/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeImageHits&filters=token_policy=577599,token_policy=577595"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

# create date:24/04/2023
@app.route('/imhits_by_policyandwidth',methods=['GET'])        
@cross_origin()
def imhits_by_policyandwidth():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/imhits_by_policyandwidth?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/imhits-by-policyandwidth/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeImageHits&filters=token_policy=577597,token_policy=577595"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/imhits_by_width',methods=['GET'])        
@cross_origin()
def imhits_by_width():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/imhits_by_width?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/imhits-by-width/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeImageHits,edgeImageHitsPercent&filters=token_policy=577598,token_policy=577597"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/imtopbytesurls_by_url_100',methods=['GET'])        
@cross_origin()
def imtopbytesurls_by_url_100():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/imtopbytesurls_by_url_100?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/imtopbytesurls-by-url-100/versions/4/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeImageVolume&filters=token_policy=577597,token_policy=577599"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})


@app.route('/imtopbytesurls_by_url',methods=['GET'])        
@cross_origin()
def imtopbytesurls_by_url():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/imtopbytesurls_by_url?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/imtopbytesurls-by-url/versions/4/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeImageVolume&filters=token_policy=577595,token_policy=577597"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/imtophiturls_by_url_100',methods=['GET'])        
@cross_origin()
def imtophiturls_by_url_100():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/imtophiturls_by_url_100?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/imtophiturls-by-url-100/versions/4/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeImageHits&filters=token_policy=577599,token_policy=577597"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/imtophiturls_by_url',methods=['GET'])        
@cross_origin()
def imtophiturls_by_url():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/imtophiturls_by_url?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/imtophiturls-by-url/versions/4/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeImageHits&filters=token_policy=577599,token_policy=577597"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})


@app.route('/imtraffic_by_imagetype',methods=['GET'])        
@cross_origin()
def imtraffic_by_imagetype():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/imtraffic_by_imagetype?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"reporting-api/v1/reports/imtraffic-by-imagetype/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeImageBytes,edgeImageBytesPercent&filters=token_policy=577596,token_policy=577599"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})


@app.route('/imtraffic_by_time',methods=['GET'])        
@cross_origin()
def imtraffic_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/imtraffic_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/imtraffic-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeImageBitsPerSecond,edgeImageBitsPerSecondLatest&filters=token_policy=577595,token_policy=577597"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/iotecconnections_by_time',methods=['GET'])        
@cross_origin()
def iotecconnections_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/iotecconnections_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/iotecconnections-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=eventsCount,eventsCountMax"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/iotectraffic_by_time',methods=['GET'])        
@cross_origin()
def iotectraffic_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/iotectraffic_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/iotectraffic-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=msgCount,msgCountMax&filters=jurisdictions=0,jurisdictions=1,msg_type=http_publish,msg_type=http_delivery"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/jwt_usage_by_endpoint',methods=['GET'])        
@cross_origin()
def jwt_usage_by_endpoint():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/jwt_usage_by_endpoint?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"reporting-api/v1/reports/jwt-usage-by-endpoint/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeHits,edgeHitsMax&filters=endpoint_id=577598,endpoint_id=577597,error_state=a,error_state=s"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})


@app.route('/jwt_usage_by_error',methods=['GET'])        
@cross_origin()
def jwt_usage_by_error():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/jwt_usage_by_error?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/jwt-usage-by-error/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeHits,edgeHitsMax&filters=endpoint_id=577598,endpoint_id=577596,error_state=p,error_state=a"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/jwt_usage_by_time',methods=['GET'])        
@cross_origin()
def jwt_usage_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/jwt_usage_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/jwt-usage-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeHits,edgeHitsMax&filters=endpoint_id=577598,endpoint_id=577597,error_state=f,error_state=o"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})


@app.route('/load_balancing_dns_traffic_all_properties',methods=['GET'])        
@cross_origin()
def load_balancing_dns_traffic_all_properties():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/load_balancing_dns_traffic_all_properties?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"reporting-api/v1/reports/load-balancing-dns-traffic-all-properties/versions/2/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=hits,startdatetime"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/load_balancing_dns_traffic_by_datacenter',methods=['GET'])        
@cross_origin()
def load_balancing_dns_traffic_by_datacenter():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/load_balancing_dns_traffic_by_datacenter?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/load-balancing-dns-traffic-by-datacenter/versions/2/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=avg_hits,hits"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})



@app.route('/load_balancing_dns_traffic_by_property',methods=['GET'])        
@cross_origin()
def load_balancing_dns_traffic_by_property():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/load_balancing_dns_traffic_by_property?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/load-balancing-dns-traffic-by-property/versions/2/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=avg_hits,hits"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/load_balancing_dns_traffic_datacenter_all_properties',methods=['GET'])        
@cross_origin()
def load_balancing_dns_traffic_datacenter_all_properties():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/load_balancing_dns_traffic_datacenter_all_properties?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/load-balancing-dns-traffic-datacenter-all-properties/versions/2/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=avg_hits,hits"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/load_balancing_dns_traffic_error_counts_by_property',methods=['GET'])        
@cross_origin()
def load_balancing_dns_traffic_error_counts_by_property():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/load_balancing_dns_traffic_error_counts_by_property?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/load-balancing-dns-traffic-error-counts-by-property/versions/2/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=domain,errorCount"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/load_balancing_dns_traffic_errors_by_property',methods=['GET'])        
@cross_origin()
def load_balancing_dns_traffic_errors_by_property():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/load_balancing_dns_traffic_errors_by_property?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/load-balancing-dns-traffic-errors-by-property/versions/2/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=answeringIp,datacenter"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})


@app.route('/load_balancing_dns_traffic_property_all_datacenters_demand_summary',methods=['GET'])        
@cross_origin()
def load_balancing_dns_traffic_property_all_datacenters_demand_summary():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/load_balancing_dns_traffic_property_all_datacenters_demand_summary?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/load-balancing-dns-traffic-property-all-datacenters-demand-summary/versions/3/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=actualLoad,alive"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/load_balancing_dns_traffic_property_all_datacenters_demand',methods=['GET'])        
@cross_origin()
def load_balancing_dns_traffic_property_all_datacenters_demand():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/load_balancing_dns_traffic_property_all_datacenters_demand?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/load-balancing-dns-traffic-property-all-datacenters-demand/versions/4/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=actualLoad,requestedLoad"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/load_balancing_dns_traffic_property_all_datacenters_liveness',methods=['GET'])        
@cross_origin()
def load_balancing_dns_traffic_property_all_datacenters_liveness():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/load_balancing_dns_traffic_property_all_datacenters_liveness?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/load-balancing-dns-traffic-property-all-datacenters-liveness/versions/3/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=notAlive,startdatetime"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/load_balancing_dns_traffic_property_all_datacenters',methods=['GET'])        
@cross_origin()
def load_balancing_dns_traffic_property_all_datacenters():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/load_balancing_dns_traffic_property_all_datacenters?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/load-balancing-dns-traffic-property-all-datacenters/versions/3/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=avg_hits,hitPercent"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/load_balancing_dns_traffic_property_load_feedback_summary',methods=['GET'])        
@cross_origin()
def load_balancing_dns_traffic_property_load_feedback_summary():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/load_balancing_dns_traffic_property_load_feedback_summary?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/load-balancing-dns-traffic-property-load-feedback-summary/versions/3/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=alive,currentLoad"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/load_balancing_dns_traffic_property_load_feedback',methods=['GET'])        
@cross_origin()
def load_balancing_dns_traffic_property_load_feedback():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/load_balancing_dns_traffic_property_load_feedback?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/load-balancing-dns-traffic-property-load-feedback/versions/3/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=currentLoad,loadPercent"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})


@app.route('/matchcategory_by_cpcode',methods=['GET'])        
@cross_origin()
def matchcategory_by_cpcode():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/matchcategory_by_cpcode?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/matchcategory-by-cpcode/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeHitsPerSecond,edgeHitsPerSecondMax&filters=delivery_type=secure,delivery_type=non-secure,ip_version=ipv4,ip_version=ipv6"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/matchcategory_by_time',methods=['GET'])        
@cross_origin()
def matchcategory_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/matchcategory_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/matchcategory-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeHitsPerSecond,edgeHitsPerSecondMax&filters=delivery_type=secure,delivery_type=non-secure,ip_version=ipv4,ip_version=ipv6"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/midgresshits_by_time',methods=['GET'])        
@cross_origin()
def midgresshits_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/midgresshits_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/midgresshits-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=midgressHitsPerSecond,midgressHitsPerSecondMax&filters=delivery_type=secure,ip_version=ipv4,ip_version=ipv6"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/opresponses_by_time',methods=['GET'])        
@cross_origin()
def opresponses_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/opresponses_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/opresponses-by-time/versions/2/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=avgResponseTime,avgResponseTimeMax&filters=ca=cacheable,ca=non_cacheable,response_code=500,response_code=200"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

# created date:25/04/2023
@app.route('/prefetchedgemetrics_by_time',methods=['GET'])        
@cross_origin()
def prefetchedgemetrics_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/prefetchedgemetrics_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/prefetchedgemetrics-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeResponsesPerSecond,edgeResponsesPerSecondLatest&filters=ca=cacheable,ca=non_cacheable"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/prefetchedgepfmetrics_by_time',methods=['GET'])        
@cross_origin()
def prefetchedgepfmetrics_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/prefetchedgepfmetrics_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/prefetchedgepfmetrics-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgePrefetchResponsesPerSecond,edgePrefetchResponsesPerSecondLatest&filters=ca=cacheable,ca=non_cacheable"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/prefetchoriginmetrics_by_time',methods=['GET'])        
@cross_origin()
def prefetchoriginmetrics_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/prefetchoriginmetrics_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/prefetchoriginmetrics-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=originPrefetchResponsesPerSecond%2CoriginPrefetchResponsesPerSecondLatest&filters=ca%3Dcacheable%2Cca%3Dnon_cacheable"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/proxytraffic_by_cpcode',methods=['GET'])        
@cross_origin()
def proxytraffic_by_cpcode():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/proxytraffic_by_cpcode?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/proxytraffic-by-cpcode/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeHitsPerSecond,edgeHitsPerSecondMax&filters=delivery_type=secure,delivery_type=non-secure,ip_version=ipv4,ip_version=ipv6"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/proxytraffic_by_time',methods=['GET'])        
@cross_origin()
def proxytraffic_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/proxytraffic_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/proxytraffic-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeHitsPerSecond,edgeHitsPerSecondMax&filters=delivery_type=secure,delivery_type=non-secure,ip_version=ipv4,ip_version=ipv6"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/pv_by_time',methods=['GET'])        
@cross_origin()
def pv_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/pv_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/pv-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=pageViewsPerSecond,pageViewsPerSecondMax"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/saastraffic_by_cust',methods=['GET'])        
@cross_origin()
def saastraffic_by_cust():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/saastraffic_by_cust?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/saastraffic-by-cust/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeBytesTotal,edgeHitsTotal&filters=appid=577596,appid=577597,http_method=delete,http_method=post"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/sriptraffic_by_time',methods=['GET'])        
@cross_origin()
def sriptraffic_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/sriptraffic_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/sriptraffic-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=bitsPerSecondMax,bytesTotal&filters=slot_id=577599,slot_id=577595"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/sxl_trafficlost_by_time',methods=['GET'])        
@cross_origin()
def sxl_trafficlost_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/sxl_trafficlost_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/sxl-trafficlost-by-time/versions/2/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=blacklistBytes,blacklistBytesTotal&filters=slot=8927,slot=140"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/sxlmapping_by_time',methods=['GET'])        
@cross_origin()
def sxlmapping_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/sxlmapping_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/sxlmapping-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=dnsRequests,dnsRequestsLatest&filters=slot=140,slot=8927"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/sxltraffic_by_time',methods=['GET'])        
@cross_origin()
def sxltraffic_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/sxltraffic_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/sxltraffic-by-time/versions/2/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=concurrentSessions,concurrentSessionsLatest&filters=slot=11838,slot=8927"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/todaytraffic_by_response',methods=['GET'])        
@cross_origin()
def todaytraffic_by_response():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/todaytraffic_by_response?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/todaytraffic-by-response/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeHits,edgeHitsPercent"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/todaytraffic_by_time_rl',methods=['GET'])        
@cross_origin()
def todaytraffic_by_time_rl():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/todaytraffic_by_time_rl?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/todaytraffic-by-time-rl/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=bytesOffload,bytesOffloadAvg&filters=response_class=4xx,response_class=2xx,response_status=success,response_status=error"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/todaytraffic_by_time',methods=['GET'])        
@cross_origin()
def todaytraffic_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/todaytraffic_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/todaytraffic-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=bytesOffload,bytesOffloadAvg&filters=response_class=0xx,response_class=3xx,response_status=success,response_status=error"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/todaytraffic_by_timeandresponseclass',methods=['GET'])        
@cross_origin()
def todaytraffic_by_timeandresponseclass():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/todaytraffic_by_timeandresponseclass?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/todaytraffic-by-timeandresponseclass/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeHitsPerSecond,originHitsPerSecond&filters=response_class=2xx,response_class=3xx,response_status=success,response_status=error"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/todaytraffic_bytes_by_cpcode',methods=['GET'])        
@cross_origin()
def todaytraffic_bytes_by_cpcode():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/todaytraffic_bytes_by_cpcode?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/todaytraffic-bytes-by-cpcode/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=bytesOffload,edgeBytes&filters=response_class=1xx,response_class=2xx,response_status=success,response_status=error"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/todaytraffic_hits_by_cpcode',methods=['GET'])        
@cross_origin()
def todaytraffic_hits_by_cpcode():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/todaytraffic_hits_by_cpcode?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/todaytraffic-hits-by-cpcode/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeHits,hitsOffload&filters=response_class=1xx,response_class=2xx,response_status=success,response_status=error"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/traffic_by_response',methods=['GET'])        
@cross_origin()
def traffic_by_response():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/traffic_by_response?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/traffic-by-response/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeHits,edgeHitsPercent"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/traffic_by_responseclass',methods=['GET'])        
@cross_origin()
def traffic_by_responseclass():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/traffic_by_responseclass?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/traffic-by-responseclass/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeHits,edgeHitsPercent"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/traffic_by_servergeo',methods=['GET'])        
@cross_origin()
def traffic_by_servergeo():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/traffic_by_servergeo?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/traffic-by-servergeo/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=edgeBytes,edgeHits&filters=country=GB,country=US,delivery_type=secure"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/traffic_by_timeandresponse',methods=['GET'])        
@cross_origin()
def traffic_by_timeandresponse():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/traffic_by_timeandresponse?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/traffic-by-timeandresponse/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeHitsPerSecond,originHitsPerSecond"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/traffic_by_timeandresponseclass',methods=['GET'])        
@cross_origin()
def traffic_by_timeandresponseclass():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/traffic_by_timeandresponseclass?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/traffic-by-timeandresponseclass/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=edgeHitsPerSecond,originHitsPerSecond"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/universallivetraffic_by_time',methods=['GET'])        
@cross_origin()
def universallivetraffic_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/universallivetraffic_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/universallivetraffic-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=hdsEdgeBitsPerSecond,hdsEdgeBitsPerSecondMax&filters=stream_id=577598,stream_id=577597"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/upsrtraffic_by_time',methods=['GET'])        
@cross_origin()
def upsrtraffic_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/upsrtraffic_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/upsrtraffic-by-time/versions/2/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=avgRouteOptimizationPercent,avgRouteOptimizationPercentMax"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/url0XXresponses_by_url',methods=['GET'])        
@cross_origin()
def url0XXresponses_by_url():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/url0XXresponses_by_url?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/url0XXresponses-by-url/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=0XXEdgeHits&filters=delivery_type=secure,url_contain=/shop,url_contain=/about"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/url2XXresponses_by_url',methods=['GET'])        
@cross_origin()
def url2XXresponses_by_url():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/url2XXresponses_by_url?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/url2XXresponses-by-url/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=200EdgeHits,206EdgeHits&filters=delivery_type=secure,url_contain=/shop,url_contain=/about"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/url3XXresponses_by_url',methods=['GET'])        
@cross_origin()
def url3XXresponses_by_url():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/url3XXresponses_by_url?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/url3XXresponses-by-url/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=302EdgeHits,304EdgeHits&filters=delivery_type=secure,url_contain=/shop,url_contain=/about"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/url4XXresponses_by_url',methods=['GET'])        
@cross_origin()
def url4XXresponses_by_url():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/url4XXresponses_by_url?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/url4XXresponses-by-url/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=404EdgeHits%2C4XXOtherEdgeHits&filters=delivery_type=secure,url_contain=/shop,url_contain=/about"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/urlbytes_by_time',methods=['GET'])        
@cross_origin()
def urlbytes_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/urlbytes_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/urlbytes-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=DAY&objectIds={objectIds}&metrics=allBytesOffload,allBytesOffloadAvg&filters=delivery_type=secure,url_contain=/shop,url_contain=/about"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/urlbytes_by_url',methods=['GET'])        
@cross_origin()
def urlbytes_by_url():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/urlbytes_by_url?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/urlbytes-by-url/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=allBytesOffload,allEdgeBytes&filters=delivery_type=secure,url_contain=/shop,url_contain=/about"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/urlerrorbytes_by_url',methods=['GET'])        
@cross_origin()
def urlerrorbytes_by_url():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/urlerrorbytes_by_url?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/urlerrorbytes-by-url/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=errorBytesOffload,errorEdgeBytes&filters=delivery_type=secure,url_contain=/shop,url_contain=/about"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/urlerrorhits_by_url',methods=['GET'])        
@cross_origin()
def urlerrorhits_by_url():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/urlerrorhits_by_url?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/urlerrorhits-by-url/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=errorEdgeHits,errorHitsOffload&filters=delivery_type=secure,url_contain=/shop,url_contain=/about"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/urlerrorresponses_by_url',methods=['GET'])        
@cross_origin()
def urlerrorresponses_by_url():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/urlerrorresponses_by_url?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"reporting-api/v1/reports/urlerrorresponses-by-url/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=0XXEdgeHits%2C4XXEdgeHits&filters=delivery_type=secure,url_contain=/shop,url_contain=/about"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/urlhits_by_time',methods=['GET'])        
@cross_origin()
def urlhits_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/urlhits_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/urlhits-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=DAY&objectIds={objectIds}&metrics=allEdgeHitsPerSecond,allEdgeHitsPerSecondMax&filters=delivery_type=secure,url_contain=/shop,url_contain=/about"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/urlhits_by_url',methods=['GET'])        
@cross_origin()
def urlhits_by_url():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/urlhits_by_url?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/urlhits-by-url/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=allEdgeHits,allHitsOffload&filters=delivery_type=secure,url_contain=/shop,url_contain=/about"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/urlresponses_by_time',methods=['GET'])        
@cross_origin()
def urlresponses_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/urlresponses_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/urlresponses-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=DAY&objectIds={objectIds}&metrics=0XXEdgeHitsMax,0XXEdgeHitsMin&filters=delivery_type=secure,url_contain=/shop,url_contain=/about"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/urlresponses_by_url',methods=['GET'])        
@cross_origin()
def urlresponses_by_url():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/urlresponses_by_url?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/urlresponses-by-url/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=0XXEdgeHits,2XXEdgeHits&filters=delivery_type=secure,url_contain=/shop,url_contain=/about"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/urlsuccessbytes_by_url',methods=['GET'])        
@cross_origin()
def urlsuccessbytes_by_url():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/urlsuccessbytes_by_url?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/urlsuccessbytes-by-url/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=successBytesOffload,successEdgeBytes&filters=delivery_type=secure,url_contain=/shop,url_contain=/about"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/urlsuccesshits_by_url',methods=['GET'])        
@cross_origin()
def urlsuccesshits_by_url():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/urlsuccesshits_by_url?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/urlsuccesshits-by-url/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=successEdgeHits,successHitsOffload&filters=delivery_type=secure,url_contain=/shop,url_contain=/about"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/urlsuccessresponses_by_url',methods=['GET'])        
@cross_origin()
def urlsuccessresponses_by_url():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/urlsuccessresponses_by_url?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/urlsuccessresponses-by-url/versions/2/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=2XXEdgeHits,3XXEdgeHits&filters=delivery_type=secure,url_contain=/shop,url_contain=/about"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/uv_by_time',methods=['GET'])        
@cross_origin()
def uv_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/uv_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/uv-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=HOUR&objectIds={objectIds}&metrics=allUniqueVisitors%2CallUniqueVisitorsAverage"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/cmlogline_by_time',methods=['GET'])        
@cross_origin()
def cmlogline_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/cmlogline_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/cmlogline-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=forwardRequestBytesPerSecond,forwardRequestBytesPerSecondLatest"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/cmreq_by_cpcode',methods=['GET'])        
@cross_origin()
def cmreq_by_cpcode():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/cmreq_by_cpcode?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/cmreq-by-cpcode/versions/1/report-data?start={start_date}&end={end_date}&objectIds={objectIds}&metrics=requestCount"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/cmreq_by_time',methods=['GET'])        
@cross_origin()
def cmreq_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/cmreq_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/cmreq-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=requestCountPerSecond,requestCountPerSecondLatest"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/ipa_trafficlost_by_time',methods=['GET'])        
@cross_origin()
def ipa_trafficlost_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/ipa_trafficlost_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"/reporting-api/v1/reports/ipa-trafficlost-by-time/versions/2/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=blacklistBytes,blacklistBytesTotal&filters=slot=11838,slot=140"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/ipamapping_by_time',methods=['GET'])        
@cross_origin()
def ipamapping_by_time():
    day_no = request.args.get('days',1,type=int)
    objectIds = request.args.get('objectIds')
    current_date = date.today()
    end_date = current_date.strftime('%Y-%m-%dT%H:%MZ')
    startdate = current_date - timedelta(days=day_no)
    start_date = startdate.strftime('%Y-%m-%dT%H:%MZ')
    # url=http://127.0.0.1:5000/ipamapping_by_time?days=19&objectIds=1349555
    if objectIds is not None:
        path = f"reporting-api/v1/reports/ipamapping-by-time/versions/1/report-data?start={start_date}&end={end_date}&interval=FIVE_MINUTES&objectIds={objectIds}&metrics=dnsRequests,dnsRequestsLatest&filters=slot=11838,slot=140"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            data = {
                "result":result.json(),
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "CPcode is required....."
        return jsonify({"msg":msg})

@app.route('/get_properties_id_and_groupid',methods=['GET'])        
@cross_origin()
def get_properties_id_and_groupid():
    # url=http://127.0.0.1:5000/get_properties_id_and_groupid
    path = f"identity-management/v3/user-admin/properties"
    if(request.method == 'GET'):
        baseurl = base_url
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token=client_token,
            client_secret=client_secret,
            access_token=access_token
        )
        result = s.get(urljoin(baseurl, path),headers=headers)
        data = {
            "result":result.json(),
            "status_code":result.status_code
        }
        return jsonify(data)
    
@app.route('/get_cpcode_by_propetiesid_groupid',methods=['GET'])        
@cross_origin()
def get_cpcode_by_propetiesid_groupid():
    propertyId = request.args.get('propertyId')
    groupId = request.args.get('groupId')
    
    # url=http://127.0.0.1:5000/get_cpcode_by_propetiesid_groupid?propertyId=11155596&groupId=234490
    # propertyId = 11155596
    # groupId = 234490
    if propertyId !="" and groupId != "":
        path = f"identity-management/v3/user-admin/properties/{propertyId}/resources?groupId={groupId}"
        if(request.method == 'GET'):
            baseurl = base_url
            s = requests.Session()
            s.auth = EdgeGridAuth(
                client_token=client_token,
                client_secret=client_secret,
                access_token=access_token
            )
            result = s.get(urljoin(baseurl, path),headers=headers)
            res = result.json()
            data = {
                "result":res[1],
                "status_code":result.status_code
            }
            return jsonify(data)
    else:
        msg = "PropertiesId and GroupId is required....."
        return jsonify({"msg":msg})





if __name__=='__main__':
    app.run(host='akamai-be.multitvsolution.com',ssl_context=("Merge.crt", "multitv.key"))
