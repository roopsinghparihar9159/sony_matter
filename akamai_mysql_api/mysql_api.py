from flask import Flask, render_template, request, redirect, url_for, session,jsonify,request,json
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import requests
from functools import wraps
from __main__ import app
#app = Flask(__name__)

cors = CORS(app,resources={r"/": {"origins": ""}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.secret_key = 'your secret key'
 
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'Password123#@!'
# app.config['MYSQL_DB'] = 'akamai'

app.config['MYSQL_HOST'] = "103.253.175.26"
app.config['MYSQL_USER'] = "api"
app.config['MYSQL_PASSWORD'] = "akamai@MTV"
app.config['MYSQL_DB'] = "akamai"
 
 
mysql = MySQL(app)

@app.route('/get_api',methods=['GET'])
@cross_origin()
def get_authentication_data():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM autheticate')
        rows = cursor.fetchall()
        cursor.close()
        # connection.close()
        all_data = list()
        for data in rows:
            data_dict = dict()
            for d in data:
                data_dict={
                    'Id':data['Id'],'UserName':data['UserName'],'LastName':data['LastName'],'FirstName':data['FirstName'],'EmailId':data['EmailId'],'Passwd':data['Passwd']
                }
            all_data.append(data_dict)
            status_code="200 Ok"
        
    data ={
        "data":all_data
    }
    return jsonify(data)

 

@app.route('/login',methods=['GET','POST'])
@cross_origin()
def login():
    msg = ''
    if request.method == 'POST':
        emailid = request.form['emailid']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        credential = f"select * from autheticate where EmailId='{emailid}' and Passwd=aes_encrypt('{password}','key1234');"
        cursor.execute(credential)
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['Id']
            session['username'] = account['UserName']

            msg = 'Logged in successfully !'
            loggedin = session['loggedin']
            id = session['id']
            username = session['username']
            data ={"msg":msg,'loggedin':loggedin,'id':id,'username':username,'status_code':200}
            return jsonify(data)
        else:
            msg = 'Incorrect username / password !'
            data ={"msg":msg}
    return jsonify(data)

@app.route('/logout')
@cross_origin()
def logout():
    if 'username' in session:
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)
        msg = "You are logout successfully...."
        status_code = '200'
    else:
        msg = "You are not login...."
        status_code = '401'
    data ={"msg":msg,'status_code':status_code}
    return jsonify(data)

@app.route('/register',methods=['POST'])
@cross_origin()
def register():
    if request.method == 'POST':
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        emailid = request.form['emailid']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = f"SELECT * FROM autheticate where EmailId='{emailid}';"
        cursor.execute(query)
        rows = cursor.fetchone()
        if rows:
            msg = "Email Id already resgister..."
            return jsonify({'msg':msg})
        elif username =="" or firstname == "" or lastname == "" or emailid == "" or password == "" or confirm_password == "":
            msg = "Please fill all the Fields mandatory!"
            return jsonify({'msg':msg})
        elif password != confirm_password:
            msg = "Password don't match...."
            return jsonify({'msg':msg})
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', emailid):
            msg = 'Invalid email address !'
            return jsonify({'msg':msg})
        elif not re.match(r'[A-Za-z0-9]+', username):
            print(username)
            msg = 'name must contain only characters and numbers !'
            return jsonify({'msg':msg})
        else:
            insert_query = f"insert into autheticate(UserName,LastName,FirstName,EmailId,Passwd,Role)values('{username}','{lastname}','{firstname}','{emailid}',aes_encrypt('{password}','key1234'),'{role}');"
            cursor.execute(insert_query)
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    return jsonify({'msg':msg})


def authenticated_resource(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)

        return redirect(url_for('login_page'))

    return decorated


if __name__=='__main__':
    #app.run(host="akamai-be.multitvsolution.com",port=5001,ssl_context=("Merge.crt", "multitv.key"))
    app.run(debug=True) 
