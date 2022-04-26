from flask import Flask, redirect, request, Response, session, make_response, render_template
from flask_mysqldb import MySQL
import os

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static/src/pages',
            template_folder='web/templates')

app.secret_key = "super secret key"

app.config['MYSQL_HOST'] = 'dcrhg4kh56j13bnu.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'rpawh9q7q2ra0ces'
app.config['MYSQL_PASSWORD'] = 'vurbee05mr0v4lgs'
app.config['MYSQL_DB'] = 'jxxv8laq46soz2mq'
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

@app.route('/', methods=['POST', 'GET'])  # redirecting to url in flask, ref: https://flask.palletsprojects.com/en/2.1.x/api/
def index():
    if 'user' in session:
        return redirect("./student-dashboard.html", code=302)
    else:
        return redirect("./login.html", code=302)


@app.route('/login', methods=['POST'])
def login():
    errorMsg = ''  # output error message if error occurred
    result = {}
    if request.method == 'POST':
        useremail = request.form['email']
        userpassword = request.form['password']
        isRememberme = bool('rememberme' in request.form and request.form['rememberme'] == 'on')
        print("useremail:" + useremail)
        print("userpassword:" + userpassword)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT user_id, user_name, user_type, score FROM User WHERE email = %s AND  pwd = %s", (useremail, userpassword))
        # Fetch one record and return result
        user = cursor.fetchone()
        if user is None:  # user not exist
            errorMsg = 'You have entered an invalid username or password!!!'
        else:
            session['user'] = user
        # Saving the Actions performed on the DB
        mysql.connection.commit()

        # Closing the cursor
        cursor.close()

        result["success"] = True if errorMsg == '' else False
        result["errorMsg"] = errorMsg
        result["data"] = user
        res = make_response(result)
        if isRememberme:
            #cookie
            res.set_cookie("email", value=str(useremail))
        else:
            res.set_cookie("email", value="", expires=0)
        return res


@app.route('/logout')
def logout():
    # remove the user from the session if it is there
    if 'user' in session:
        session.pop('user', None)

    return redirect('/')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
