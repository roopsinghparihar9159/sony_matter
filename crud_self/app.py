from flask import *
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    con = sql.connect("employee.db")
    con.row_factory=sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    collection_list=[]
    for i in rows:
        data=dict()
        for j in i:
            # data['id']=i['id']
            # data['name']=i['name']
            # data['contact']=i['contact']
            # data['address']=i['address']
            # data['pincode']=i['pincode']
            data={
                'id':i['id'],'name':i['name'],'contact':i['contact'],'address':i['address'],'pincode':i['pincode']
            }
        collection_list.append(data)
        # print(data)
    print(collection_list)
    
    return render_template("index.html",rows=rows)
    # return jsonify(collection_list)


# @app.route('/api')
# def api():
#     con = sql.connect("employee.db")
#     con.row_factory=sql.Row
#     cur = con.cursor()
#     cur.execute("SELECT * FROM users")
#     rows = cur.fetchall()
#     collection_list=[]
#     for i in rows:
#         data=dict()
#         for j in i:
#             data={
#                 'id':i['id'],'name':i['name'],'contact':i['contact'],'address':i['address'],'pincode':i['pincode']
#             }
#         collection_list.append(data)
        
#     print(collection_list)
    
#     return jsonify(collection_list)


@app.route('/add_user',methods=["POST","GET"])
def add_user():
    if request.method == "POST":
        name = request.form["name"]
        contact = request.form["contact"]
        address = request.form["address"]
        pincode = request.form["pincode"]
        con = sql.connect("employee.db")
        cur = con.cursor()
        cur.execute("INSERT INTO users(NAME,CONTACT,ADDRESS,PINCODE) values(?,?,?,?)",(name,contact,address,pincode))
        con.commit()
        flash('User added successfully','Success')
        return redirect(url_for("index"))
    return render_template("add_user.html")

@app.route('/edit_user/<string:id>',methods=["POST","GET"])
def edit_user(id):
    if request.method == "POST":
        name = request.form["name"]
        contact = request.form["contact"]
        address = request.form["address"]
        pincode = request.form["pincode"]
        con = sql.connect("employee.db")
        cur = con.cursor()
        cur.execute("UPDATE users set NAME=?,CONTACT=?,ADDRESS=?,PINCODE=? WHERE ID=?",(name,contact,address,pincode,id))
        con.commit()
        flash("User updated Successfully...","Success")
        return redirect(url_for("index"))
    con = sql.connect("employee.db")
    con.row_factory=sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE ID=?",(id,))
    data=cur.fetchone()
    return render_template("edit_user.html",datas=data)

@app.route('/delete_user/<string:id>',methods=["GET"])
def delete_user(id):
    if request.method == "GET":
        con = sql.connect("employee.db")
        cur = con.cursor()
        cur.execute("DELETE FROM users WHERE ID=?",(id,))
        con.commit()
        flash("User deleted Successfully..","Deleted")
    return redirect(url_for("index"))

# @app.route('/delete/api/<string:id>',methods=["POST"])
# def delete_api(id):
#     print(id)
#     if request.method == "POST":
#         con = sql.connect("employee.db")
#         cur = con.cursor()
#         cur.execute("DELETE FROM users WHERE ID=?",id)
#         con.commit()
#         data=dict()
#         # flash("User deleted Successfully..","Deleted")
#         data['msg']="User deleted Successfully"
#     return jsonify(data)

if __name__=="__main__":
    app.secret_key='admin123'
    app.run(debug=True)