from flask import Flask, redirect, url_for, request, jsonify, Response, session
from flask_mysqldb import MySQL
from flask_talisman import Talisman
import os

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static/src/pages',
            template_folder='web/templates')

Talisman(app)

app.config['MYSQL_HOST'] = 'dcrhg4kh56j13bnu.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'rpawh9q7q2ra0ces'
app.config['MYSQL_PASSWORD'] = 'vurbee05mr0v4lgs'
app.config['MYSQL_DB'] = 'jxxv8laq46soz2mq'

mysql = MySQL(app)


@app.route('/')
def hello():
    return redirect("./login.html", code=302)

@app.route('/login', methods=['POST'])
def login():
    errorMsg = ''  # output error message if error occurred
    if request.method == 'POST':
        useremail = request.form['email']
        userpassword = request.form['password']
        print("useremail:" + useremail)
        print("userpassword:" + userpassword)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM User WHERE email = %s AND  pwd = %s", (useremail, userpassword))
        row_headers = [h[0] for h in cursor.description]  # extract row headers
        # Fetch one record and return result
        user = cursor.fetchone()
        if user is None:  # user not exist
            errorMsg = 'You have entered an invalid username or password!!!'
        # Saving the Actions performed on the DB
        mysql.connection.commit()

        # Closing the cursor
        cursor.close()
        result = {}
        result["success"] = True if errorMsg == '' else False
        result["errorMsg"] = errorMsg
        result["data"] = user

        return result

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
