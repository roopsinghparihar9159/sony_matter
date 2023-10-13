from flask import *
import sqlite3 as sql
app.Flask('__name__')

@app.route('api/',methods=['POST'])
def fetch_alldata():
    con = sql.connect("employee.db")
    con.row_factory=sql.Raw
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

if __name__=="__main__":
    app.secret_key='admin123'
    app.run(debug=True)