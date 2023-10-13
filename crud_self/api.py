from flask import *
import sqlite3 as sql
app = Flask('__name__')

@app.route('/api')
def fetch_alldata():
    con = sql.connect("employee.db")
    con.row_factory=sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    all_data = list()
    for data in rows:
        data_dict = dict()
        for d in data:
            data_dict={
                'id':data['id'],'name':data['name'],'contact':data['contact'],'address':data['address'],'pincode':data['pincode']
            }
            all_data.append(data_dict)
    return jsonify(all_data)


@app.route('/add_user',methods=["POST"])
def add_user():
    if request.method == "POST":
        name = request.form['name']
        contact = request.form['contact']
        address = request.form['address']
        pincode = request.form["pincode"]
        con = sql.connect('employee.db')
        cur = con.cursor()
        cur.execute("INSERT INTO users(NAME,CONTACT,ADDRESS,PINCODE) values(?,?,?,?)",(name,contact,address,pincode))
        con.commit()
        msg='User Record save successfully.....'
    return jsonify({'msg':msg})


@app.route('/api_send',methods=["POST"])
def send_data():
    if request.method == "POST":
        streamkey = request.form['streamkey']
        status = request.form['status']
    return jsonify({'streamkey':streamkey,'status':status})

@app.route('/start',methods=["POST"])
def start():
    if request.method == "POST":
        streamkey = request.form['streamkey']
        type = request.form['type']
        publishing_url = request.form['publishing_url']
        create = f'tmux ffmpeg -i url/{streamkey} -codec copy -f flv {publishing_url}'
        print('create:',create)
    return jsonify({'streamkey':streamkey,'type':type,'publishing_url':publishing_url})


@app.route('/stop',methods=["POST"])
def stop():
    if request.method == "POST":
        streamkey = request.form['streamkey']
        type = request.form['type']
        stop = f'kill {streamkey}'
        print('stop:',stop)
    return jsonify({'streamkey':streamkey,'type':type})


if __name__=="__main__":
    # app.secret_key='admin123'
    app.run(debug=True)