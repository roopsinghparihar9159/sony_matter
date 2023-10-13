from flask import *
import sqlite3 as sql

app=Flask(__name__)


@app.route('/')
@app.route('/index',methods=["POST","GET"])
def index():

    return render_template('index.html')

@app.route('/all_user',methods=["POST","GET"])
def all_user():
    if request.method == "GET":
        con = sql.connect('employee.db')
        con.row_factory=sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        collection_list=[]
        for i in rows:
            data=dict()
            for j in i:
                data={
                    'id':i['id'],'name':i['name'],'contact':i['contact'],'address':i['address']
                }
            collection_list.append(data)
    return jsonify(collection_list)
    

@app.route('/add_user',methods=["POST"])
def add_user():
    if request.method == "POST":
        name = request.form['name']
        contact = request.form['contact']
        address = request.form['address']
        con = sql.connect('employee.db')
        cur = con.cursor()
        cur.execute("INSERT INTO users(NAME,CONTACT,ADDRESS) VALUES(?,?,?)",(name,contact,address))
        con.commit()
        msg='Save'
    return jsonify({'msg':msg})


@app.route("/edit_user/api/<string:id>",methods=['POST','GET'])
def edit_user(id):
    con=sql.connect("employee.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from users where ID=?",(id,))
    rows=cur.fetchone()
    print(dict(rows))
    user_data= dict(rows)
    msg='Save'
    return jsonify({'msg':msg},user_data)


@app.route("/update_user/api/",methods=['POST','GET'])
def update_user():
    if request.method=='POST':
        id=request.form['id']
        name=request.form['name']
        contact=request.form['contact']
        address=request.form['address']
        con=sql.connect("employee.db")
        cur=con.cursor()
        cur.execute("update users set NAME=?,CONTACT=?,ADDRESS=? where ID=?",(name,contact,address,id))
        con.commit()
        msg='Update'
        print('Update')
        return jsonify({'msg':msg})
    msg='Unsuccessfull'
    return jsonify({'msg':msg})


@app.route('/delete/api/<string:id>',methods=["POST"])
def delete_api(id):
    print(id)
    if request.method == "POST":
        con = sql.connect("employee.db")
        cur = con.cursor()
        cur.execute("DELETE FROM users WHERE ID=?",(id,))
        con.commit()
        data=dict()
        # flash("User deleted Successfully..","Deleted")
        data['msg']="User deleted Successfully"
    return jsonify(data)


if __name__=="__main__":
    app.run(debug=True)
