from flask import Flask, redirect, request, Response, session
from flask_mysqldb import MySQL
from flask_talisman import Talisman
import os

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static/src/pages',
            template_folder='web/templates')

app.secret_key = "super secret key"

# Forces all connects to https
# Reference: https://github.com/GoogleCloudPlatform/flask-talisman
#Talisman(app, content_security_policy=None)

app.config['MYSQL_HOST'] = 'dcrhg4kh56j13bnu.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'rpawh9q7q2ra0ces'
app.config['MYSQL_PASSWORD'] = 'vurbee05mr0v4lgs'
app.config['MYSQL_DB'] = 'jxxv8laq46soz2mq'

mysql = MySQL(app)

@app.route('/') # redirecting to url in flask, ref: https://flask.palletsprojects.com/en/2.1.x/api/
def index():
    if 'email' in session:
        return redirect("./student-dashboard.html", code=302)
    else:
        return redirect("./login.html", code=302)

@app.route('/login', methods=['POST'])
def login():
    errorMsg = ''  # output error message if error occurred
    if request.method == 'POST':
        useremail = request.form['email']
        userpassword = request.form['password']
        isRememberme = bool(request.form.get('rememberme[]'))
        print("useremail:" + useremail)
        print("userpassword:" + userpassword)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM User WHERE email = %s AND  pwd = %s", (useremail, userpassword))
        row_headers = [h[0] for h in cursor.description]  # extract row headers
        # Fetch one record and return result
        user = cursor.fetchone()
        if user is None:  # user not exist
            errorMsg = 'You have entered an invalid username or password!!!'
        else:
            if isRememberme:
                session['email'] = request.form['email']
        # Saving the Actions performed on the DB
        mysql.connection.commit()

        # Closing the cursor
        cursor.close()
        result = {}
        result["success"] = True if errorMsg == '' else False
        result["errorMsg"] = errorMsg
        result["data"] = user

        return result

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    if 'email' in session:
        session.pop('email', None)

    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
