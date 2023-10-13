from flask import Flask, request
import json, time, requests,os, ast
from db_connection import *
app = Flask(__name__)
from datetime import datetime
now = datetime.now()
from flask_cors import cross_origin

#? transcoderAPI's
def fileWriting(file_loc, data):
	f = open(file_loc, "w+" )
	f.write(f'{data}\n')
	f.close()

def json_entryTOdb(json_data):
    if 'error' in json_data[0].keys(): print("No record Found",time.asctime())
    else:
        # print("json_data",json_data) # CONTENT_DATA = json_data[0]['content_id']
        os.system(f"echo '{time.asctime()}/n{json_data}/n########' >> logs/jsonn.log")
        for content_data in json_data:
            print("CONTENT_DATA",content_data['content_id'])
            CONTENT_id = content_data['content_id'][0]['content_id']
            # print("CONTENT_ID =",CONTENT_id)
            FILE_LOC = f"/data/transcoder/transcoder_json/{CONTENT_id}.json"
            if os.path.exists(FILE_LOC): os.system(f"mv {FILE_LOC} /data/transcoder/backup_json/") # os.remove(FILE_LOC)
            fileWriting(FILE_LOC,content_data)
            print("*********")
            base_URL = content_data['content_id'][0]['base_url']
            cur,db = dbconn()
            app_id = content_data['content_id'][0]['app_id']
            print("APP_ID: ",app_id,"CONTENT_ID =",CONTENT_id,"BASE_url: ",base_URL)
            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            # sql_Quer = f"INSERT INTO LOC_transcoder (app_id, content_id,path,dt,qc,isTranscoded,isUploaded,spriteGen) VALUES ({app_id}, {CONTENT_id},'{FILE_LOC}','{formatted_date}','0','0','0','0')"
            sql_Quer = f"insert into LOC_transcoder (app_id, content_id,path,dt,qc,isTranscoded,isUploaded,spriteGen) VALUES ({app_id}, {CONTENT_id},'{FILE_LOC}','{formatted_date}','0','0','0','0') on duplicate key update dt='{formatted_date}',path='{FILE_LOC}',qc='0',isTranscoded='0',isUploaded='0',app_id={app_id},content_id={CONTENT_id},spriteGen='0'"
            print(sql_Quer)
            cur.execute(sql_Quer)
            db.commit()
            db.close()
            p2 = requests.post("https://"+base_URL+"/crons/transcodeupdate", verify=False, data = {'id': app_id, 'content_id': CONTENT_id, 'status': 'inprocess'})
            print(p2.status_code, p2.reason)

@app.route("/json_entry",methods=['POST','GET'])
def json_reader():
	if request.method == 'POST' and 'json_bin' in request.form:
		JSON_data = request.form['json_bin']
		#print(JSON_data,type(JSON_data)) # data = request.files['json_file'] # print(data) # print(request.files.get(data)) # print(data.filename) # data.save("./"+data.filename) # f = open("./"+data.filename)
		Json_data = json.loads(JSON_data) # Closing file f.close()
		#print(Json_data) #content_id = Json_data[0]['content_id'][0]['content_id'] # FILE_LOC = f"/data/transcoder/transcoder_json/{content_id}.json" # fileWriting(FILE_LOC,Json_data) #print(Json_data)
		json_entryTOdb(Json_data)
		return {"code":"1","result":"json posted"} #'done'
	else:
		print("NO json_BIN")
		return {"code":"0","result":"json posted failed"} #'done'

@app.route("/status_getter",methods=['POST','GET'])
def status_getter():
    if request.method == 'POST' and 'app_id' in request.form:
        # percentage = request.form['percentage']
        app_id = request.form['app_id']
        content_id = request.form['content_id']
        # quer = f"UPDATE LOC_transcoder SET percentage = '{percentage}%' WHERE app_id like '{app_id}' and content_id like '{content_id}';"
        cur,db = dbconn()
        cur.execute(f"select percentage from LOC_transcoder WHERE app_id = '{app_id}' and content_id = '{content_id}' limit 0,1;")
        dbData=cur.fetchone()
        if(dbData is not None):
            percentage = dbData
            db.close()
            return {"code":"1","app_id":app_id,"content_id":content_id,"result":percentage}
        else:
            db.close()
            return {"code":"1","app_id":app_id,"content_id":content_id,"result":"NONE"}
        # cur.execute(quer) # db.commit()
    else:
        print("NO json_BIN")
        return {"code":"0","result":"No proper Inputs"} #'done'


@app.route("/list") #method for listing recent data
@cross_origin(origin="*")
def list():
    query="select * from LOC_transcoder where qc in ('Ok','-1') and istranscoded in ('key','0','-1','Ok','Tr-Fail','P-FailD','P-Fail') and isUploaded='0' order by dt desc limit 0,50;" #select * from LOC_transcoder order by dt desc limit 0,100;
    cur,db=dbconn()
    cur.execute(query)
    row_headers = [x[0] for x in cur.description]
    data = cur.fetchall()
    db.close()
    datadump=[]
    for result in data:
        datadump.append(dict(zip(row_headers,result)))
    return {"result":datadump}
    # for row in data: #     val={} #     val['app_id']=row[0] #     val['content_id']=row[1] #     val['qc']=row[3] #     val['Transcoding']=row[4] #     val['Uploaded']=row[7]  #     val['sprite']=row[9] #     datadump.append(val) # return(json.dumps(datadump, indent=4))

@app.route("/list_id/<id>") #method for listing recent data
@cross_origin(origin="*")
def list_id(id):
    query=f"select * from LOC_transcoder where content_id='{id}';"
    cur,db=dbconn()
    cur.execute(query)
    row_headers = [x[0] for x in cur.description]
    data = cur.fetchall()
    db.close()
    # print(data,type(data),len(data))
    if len(data)>0: 
        print("Notnone")
        datadump=[]
        for result in data:
            datadump.append(dict(zip(row_headers,result)))
        path= datadump[0]['path']
        f=open(path,'r')
        fdata=f.read()
        f.close() #data = ast.literal_eval(self.removejsonchar(data))
        fdata=ast.literal_eval(fdata) 
        return {"j_data":fdata,"dbdump":datadump}#fdata #json.dumps(datadump, default=str) #print("return db data",json.dumps(datadump, default=str))
    else : 
        return "No Data"

@app.route("/list_aud/<app_id>") #method for listing recent data
@cross_origin(origin="*")
def list_aud(app_id):
    query=f"select * from LOC_transcoder where app_id='{id}' and isTranscoded='0' and qc='Ok' limit 0,1;"
    cur,db=dbconn()
    cur.execute(query)
    row_headers = [x[0] for x in cur.description]
    data = cur.fetchall()
    db.close()
    # print(data,type(data),len(data))
    if len(data)>0: 
        print("Notnone")
        datadump=[]
        for result in data:
            datadump.append(dict(zip(row_headers,result)))
        path= datadump[0]['path']
        f=open(path,'r')
        fdata=f.read()
        f.close() #data = ast.literal_eval(self.removejsonchar(data))
        fdata=ast.literal_eval(fdata) 
        return {"j_data":fdata,"dbdump":datadump}#fdata #json.dumps(datadump, default=str) #print("return db data",json.dumps(datadump, default=str))
    else : 
        return "No Data"

@app.route("/process_details") #method for listing recent data
@cross_origin(origin="*")
def process_details():
    start_dt = '2023-06-01 00:00:00'
    end_dt = '2023-07-10 23:59:00'
    query=f"select COUNT(if(isTranscoded in ('-1','Ok') and isUploaded='0' ,1,null)) as Inprocess, COUNT(if(isTranscoded='Ok' and isUploaded in ('Ok','ver'),1,null)) as Completed, COUNT(if(isTranscoded='0',1,null)) as Pending, COUNT(if(isTranscoded='Tr-Fail',1,null)) as TrFail,COUNT(if(isTranscoded in ('P-FailD','P-Fail'),1,null)) as PcFail, COUNT(if(isTranscoded not like 'NA',1,null)) as Total from LOC_transcoder where qc='Ok' and dt between '{start_dt}' and '{end_dt}' and app_id='1061' order by dt;" #select * from LOC_transcoder order by dt desc limit 0,100;
    cur,db=dbconn()
    cur.execute(query)
    row_headers = [x[0] for x in cur.description]
    data = cur.fetchall()
    db.close()
    datadump=[]
    for result in data:
        datadump.append(dict(zip(row_headers,result)))
    datadump[0]['Start_dt'] = start_dt
    datadump[0]['end_dt'] = end_dt
    return {"result":datadump}

@app.route("/regain/<id>") # method for retranscode any content
@cross_origin(origin="*")
def regain(id):
    query=f"update LOC_transcoder set isTranscoded='0' where content_id='{id}'"
    cur,db=dbconn()
    cur.execute(query)
    db.commit()
    db.close()
    return{'status':'record updated'}

@app.route("/regain_qc/<id>") # method for retranscode any content
def regain_qc(id):
    query=f"update LOC_transcoder set qc='0',isTranscoded='0',isUploaded='0' where content_id='{id}'"
    cur,db=dbconn()
    cur.execute(query)
    db.commit()
    db.close()
    return{'status':'record updated'}

@app.route("/transcoderjob_data/<trans_details>")
def transcoderjob_data(trans_details):
    cur,db = dbconn()
    # cur.execute("select app_id,content_id,path,filename,gpu_compatible from LOC_transcoder where isTranscoded='0' and qc='Ok' limit 0,1;") #todo for only specific content
    cur.execute(f"select * from LOC_transcoder where isTranscoded='0' and qc='Ok' and trans_details='{trans_details}'  order by dt desc limit 0,1;") #and app_id not like '717'
    row_headers = [x[0] for x in cur.description]
    data = cur.fetchall()
    db.close()
    # print(data,type(data),len(data))
    if len(data)>0: 
        print("Notnone")
        datadump=[]
        for result in data:
            datadump.append(dict(zip(row_headers,result)))
        path= datadump[0]['path']
        f=open(path,'r')
        fdata=f.read()
        f.close() #data = ast.literal_eval(self.removejsonchar(data))
        fdata=ast.literal_eval(fdata) 
        return {"j_data":fdata,"dbdump":datadump}#fdata #json.dumps(datadump, default=str) #print("return db data",json.dumps(datadump, default=str))
    else : 
        return "No Data" #print("None")

@app.route("/status_live") #method for checking api working or not
def status_live():
    return "True"

@app.route("/dbstatus") #method for checking api working or not
def dbstatus():
    cur,db=dbconn()
    db.close()
    return "True"

@app.route("/update_db",methods=['POST','GET'])
def update_db():
    if request.method == 'POST' and 'content_id' in request.form and 'app_id' in request.form and 'file_name' in request.form and 'typee' in request.form and 'value' in request.form and 'percentage' in request.form:
        content_id = request.form['content_id']
        app_id = request.form['app_id']
        file_name = request.form['file_name'] 
        typee = request.form['typee'] #transcoder=isTranscoded | uploader=isUploaded | sprite_gen=spriteGen
        value = request.form['value'] #0 | -1 | Ok | failed ...etc
        percentage = request.form['percentage'] #1% | 25% | 75%
        typee = "isTranscoded" if typee == "transcoder" else ("isUploaded" if typee == "uploader" else ("spriteGen" if typee == "sprite_gen" else ("ispackaging" if typee == "packager" else "")))
        cur,db=dbconn()
        cur.execute(f"update LOC_transcoder set {typee}='{value}',percentage='{percentage}' where filename='{file_name}' and app_id='{app_id}' and content_id='{content_id}';")
        db.commit()
        db.close()
        return {"result":"DB Updated","data":[content_id,app_id,file_name,typee,value,percentage]} #'done'
    else:
        print("NO All fields")
        return {"code":"0","result":"please post all fields"} #'done'


@app.route("/spritejob_data/<trans_details>")
def spritejob_data(trans_details):
    cur,db = dbconn()
    # cur.execute("select app_id,content_id,path,filename,gpu_compatible from LOC_transcoder where isTranscoded='Ok' and qc='Ok' and isUploaded='Ok' and spriteGen='0' limit 0,1;") #todo for only specific content
    cur.execute(f"select * from LOC_transcoder where isTranscoded='Ok' and qc='Ok' and isUploaded='Ok' and spriteGen='0' and trans_details='{trans_details}' order by dt desc limit 0,1;")
    row_headers = [x[0] for x in cur.description]
    data = cur.fetchall()
    db.close()
    # print(data,type(data),len(data))
    if len(data)>0: 
        print("Notnone")
        datadump=[]
        for result in data:
            datadump.append(dict(zip(row_headers,result)))
        path= datadump[0]['path']

        f=open(path,'r')
        fdata=f.read()
        f.close() #data = ast.literal_eval(self.removejsonchar(data))
        fdata=ast.literal_eval(fdata) 
        # print("DATA: ",data)
        return {"j_data":fdata,"dbdump":datadump}#fdata #json.dumps(datadump, default=str) #print("return db data",json.dumps(datadump, default=str))
    else :  return "No Data" #print("None")

#todo QC API's #########################
@app.route("/qcjob_data")
def qcjob_data():
    cur,db = dbconn()
    # cur.execute("select app_id,content_id,path from LOC_transcoder where qc='0' limit 0,1;") #todo for only specific content
    cur.execute("select * from LOC_transcoder where qc='0' order by dt desc limit 0,1;")
    row_headers = [x[0] for x in cur.description]
    data = cur.fetchall()
    db.close()
    # print(data,type(data),len(data))
    if len(data) > 0: 
        print("Notnone")
        datadump = []
        for result in data:
            datadump.append(dict(zip(row_headers,result)))
        path= datadump[0]['path']

        f = open(path,'r')
        fdata = f.read()
        f.close() #data = ast.literal_eval(self.removejsonchar(data))
        # print(fdata)
        # fdata = ast.literal_eval(fdata) 
        return {"j_data":fdata,"dbdump":datadump}#fdata #json.dumps(datadump, default=str) #print("return db data",json.dumps(datadump, default=str))
    else :  return "No Data" #print("None")

@app.route("/QCupdate_db",methods=['POST','GET'])
def QCupdate_db():
    if request.method == 'POST' and 'content_id' in request.form and 'app_id' in request.form and 'value' in request.form and 'trans_details' in request.form:
        content_id = request.form['content_id']
        app_id = request.form['app_id']
        value = request.form['value'] #0 | -1 | Ok | failed ...etc
        trans_details = request.form['trans_details']
        cur,db=dbconn()
        cur.execute(f"update LOC_transcoder set qc='{value}',trans_details='{trans_details}' where app_id='{app_id}' and content_id='{content_id}';")
        db.commit()
        db.close()
        return {"result":"DB Updated","data":[content_id,app_id,"qc",value]} #'done'
    else:
        print("NO All fields")
        return {"code":"0","result":"please post all fields"} #'done'

@app.route("/QCupdate_file",methods=['POST','GET'])
def QCupdate_file():
    if request.method == 'POST' and 'content_id' in request.form and 'app_id' in request.form and 'file_name' in request.form and 'value' in request.form:
        content_id = request.form['content_id']
        app_id = request.form['app_id']
        file_name = request.form['file_name'] 
        value = request.form['value'] #0 | -1 | Ok | failed ...etc
        cur,db=dbconn()
        cur.execute(f"update LOC_transcoder set filename='{file_name}',qc='{value}' where app_id='{app_id}' and content_id='{content_id}';")
        db.commit()
        db.close()
        return {"result":"DB Updated","data":[content_id,app_id,file_name]} #'done'
    else:
        print("NO All fields")
        return {"code":"0","result":"please post all fields"} #'done'

@app.route("/QC_finalUpdate",methods=['POST','GET'])
def QC_finalUpdate():
    if request.method == 'POST' and 'content_id' in request.form and 'app_id' in request.form and 'file_name' in request.form and 'gpuvalue' in request.form and 'qcc' in request.form:
        content_id = request.form['content_id']
        app_id = request.form['app_id']
        file_name = request.form['file_name'] 
        qcc = request.form['qcc'] #0 | -1 | Ok | failed ...etc
        gpuvalue = request.form['gpuvalue']
        cur,db = dbconn()
        cur.execute(f"update LOC_transcoder set qc='{qcc}',gpu_compatible={gpuvalue},percentage='5%' where filename='{file_name}' and app_id='{app_id}' and content_id='{content_id}';")
        db.commit()
        db.close()
        return {"result":"DB Updated","data":[content_id,app_id,file_name]} #'done'
    else:
        print("NO All fields")
        return {"code":"0","result":"please post all fields"} #'done'
#todo QC API's #########################

@app.route("/packagerjob_data")
def packagerjob_data():
    cur,db = dbconn()
    # cur.execute("select app_id,content_id,path,filename,gpu_compatible from LOC_transcoder where isTranscoded='0' and qc='Ok' limit 0,1;") #todo for only specific content
    cur.execute("select * from LOC_transcoder where isTranscoded='Ok' and qc='Ok' and ispackaging='0' limit 0,1;")
    row_headers = [x[0] for x in cur.description]
    data = cur.fetchall()
    db.close()
    # print(data,type(data),len(data))
    if len(data) > 0: 
        print("Notnone")
        datadump=[]
        for result in data:
            datadump.append(dict(zip(row_headers,result)))
        path = datadump[0]['path']
        f = open(path,'r')
        fdata = f.read()
        f.close() #data = ast.literal_eval(self.removejsonchar(data))
        fdata = ast.literal_eval(fdata)
        return {"j_data":fdata,"dbdump":datadump}#fdata #json.dumps(datadump, default=str) #print("return db data",json.dumps(datadump, default=str))
    else : 
        return "No Data" #print("None")
#? transcoderAPI's

@app.route("/updatetime/<id>") # method for retranscode any content
def updatetime(id):
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    query=f"update LOC_transcoder set complete_tm='{formatted_date}' where content_id='{id}'"
    cur,db=dbconn()
    cur.execute(query)
    db.commit()
    db.close()
    return{'status':'record updated'}

if __name__=="__main__":
	app.run(host='0.0.0.0',port=7005,debug=True)
