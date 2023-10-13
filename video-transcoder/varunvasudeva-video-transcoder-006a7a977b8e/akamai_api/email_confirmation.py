from flask import Flask, render_template, request, redirect, url_for, session,jsonify,request
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail
from flask_mail import Message
import datetime
from datetime import datetime

app = Flask(__name__)


app.secret_key = 'your secret key'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Password123#@!'
app.config['MYSQL_DB'] = 'email_confirmation'

 
mysql = MySQL(app)


app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'ranusinghjhansi59@gmail.com',
    MAIL_PASSWORD = 'adgirvsgxtgeckes'
)
app.config['SECURITY_PASSWORD_SALT'] = 'fkslkfsdlkfnsdfnsfd'
app.config['MAIL_DEFAULT_SENDER'] = 'ranusinghjhansi59@gmail.com'

mail = Mail(app)

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config["MAIL_DEFAULT_SENDER"],
    )
    mail.send(msg)


def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=app.config["SECURITY_PASSWORD_SALT"])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
        )
        return email
    except Exception:
        return False

@app.route("/confirm/<token>")
def confirm_email(token):
    email = confirm_token(token)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = f"SELECT * FROM email_confirm where EmailId='{email}';"
    cursor.execute(query)
    account = cursor.fetchone()
    email_id = account['EmailId']
    is_confirmed = account['is_confirmed']
    if is_confirmed:
        msg = "Account already confirmed."
        return jsonify({'msg':msg})
    # email = confirm_token(token)
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # query = f"SELECT * FROM email_confirm where EmailId='{email}';"
    # cursor.execute(query)
    # account = cursor.fetchone()
    # email_id = account['EmailId']
    if account:
        is_confirmed = 1
        confirmed_on = datetime.now()
        update_query = f"UPDATE email_confirm SET is_confirmed='{is_confirmed}',confirmed_on='{confirmed_on}' WHERE EmailId='{email_id}';"
        cursor.execute(update_query)
        mysql.connection.commit()
        msg = "You have confirmed your account. Thanks!"
        return jsonify({'msg':msg})
    else:
        msg = "The confirmation link is invalid or has expired."
        return jsonify({'msg':msg})


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        emailid = request.form['emailid']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        insert_query = f"insert into email_confirm(UserName,LastName,FirstName,EmailId,Passwd)values('{username}','{lastname}','{firstname}','{emailid}',aes_encrypt('{password}','key1234'));"
        # session['id'] = account['Id']
        # session['emailid'] = account['emailid']
        # email_id = account['emailid']
        cursor.execute(insert_query)
        mysql.connection.commit()
        # msg = 'You have successfully registered !'
        token = generate_token(emailid)
        confirm_url = url_for("confirm_email", token=token, _external=True)
        html = render_template("accounts/confirm_email.html", confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(emailid, subject, html)
        msg = "A confirmation email has been sent via email."
    return jsonify({'msg':msg})


if __name__=='__main__':
    app.run(debug=True)
    
    



# https://www.freecodecamp.org/news/setup-email-verification-in-flask-app/