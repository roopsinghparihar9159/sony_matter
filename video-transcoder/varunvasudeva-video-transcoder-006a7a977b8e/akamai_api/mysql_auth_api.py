from flask import Flask, render_template, request, redirect, url_for, session,jsonify,request
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import requests
from functools import wraps

app = Flask(__name__)
 
app.secret_key = 'your secret key'
 
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'Password123#@!'
# app.config['MYSQL_DB'] = 'akamai'

app.config['MYSQL_HOST'] = "103.253.175.26"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "root"
app.config['MYSQL_DB'] = "akamai"
 
 
mysql = MySQL(app)

@app.route('/get_api',methods=['GET'])
def get_authentication_data():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM auth_table_demo')
        rows = cursor.fetchall()
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

@app.route("/display")
def display():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM auth_table_demo WHERE UserName = % s',(session['username'], ))
        account = cursor.fetchone()
        print(account['UserName'])
        return render_template("accounts/display.html", account=account)
        
    return jsonify({'msg':"You are not login.Please login and get details"})
    # return redirect(url_for('login'))
 

@app.route('/login',methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST':
        emailid = request.form['emailid']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        credential = f"select * from auth_table_demo where EmailId='{emailid}' and Passwd=aes_encrypt('{password}','key1234');"
        cursor.execute(credential)
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['Id']
            session['username'] = account['UserName']

            print(session)
            msg = 'Logged in successfully !'
            data ={"msg":msg,"session":session,'status_code':200}
            return jsonify(data)
        else:
            msg = 'Incorrect username / password !'
            data ={"msg":msg}
    return jsonify(data)

@app.route('/logout')
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
def register():
    if request.method == 'POST':
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        emailid = request.form['emailid']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = f"SELECT * FROM auth_table_demo where EmailId='{emailid}';"
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
            insert_query = f"insert into auth_table_demo(UserName,LastName,FirstName,EmailId,Passwd)values('{username}','{lastname}','{firstname}','{emailid}',aes_encrypt('{password}','key1234'));"
            cursor.execute(insert_query)
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    return jsonify({'msg':msg})



@app.route('/login_page',methods=['GET','POST'])
def login_page():
    return render_template("accounts/login.html")

def authenticated_resource(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)

        return redirect(url_for('login_page'))

    return decorated


@app.route('/login_user',methods=['GET','POST'])
@authenticated_resource
def login_user():
    baseurl = 'http://127.0.0.1:5000'
    path = 'login'
    headers = {"Accept": "application/json"}

    result = requests.get('http://103.253.175.26:5000/get_adaptive_media_delivery_historical_data?cpcodes=1456363,1456910&dimensions=2&metrics=107,221,7,455,9,12&days=30',headers=headers)
    print(result)
    for x in result:
        print(x)
    # return render_template("accounts/login.html")
    return 'Hellow world'




if __name__=='__main__':
    app.run(debug=True)
    