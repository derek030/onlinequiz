# Author: Chun Hin Chan(103846278)
# main python file

from flask import Flask
from flask_mysqldb import MySQL
import os

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static/pages',
            template_folder='web/templates')

app.secret_key = "super secret key"

app.config['MYSQL_HOST'] = 'dcrhg4kh56j13bnu.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'rpawh9q7q2ra0ces'
app.config['MYSQL_PASSWORD'] = 'vurbee05mr0v4lgs'
app.config['MYSQL_DB'] = 'jxxv8laq46soz2mq'
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


@app.route('/', methods=['POST', 'GET'])
# redirecting to url in flask, ref: https://flask.palletsprojects.com/en/2.1.x/api/
def index():
    if 'user' in session:
        print(session['user'])
        user = session['user']
        userType = user['user_type']
        if userType == 'Tutor':
            return redirect("./tutor-dashboard.html", code=302)
        else:
            return redirect("./student-dashboard.html", code=302)
    else:
        return redirect("./login.html", code=302)

# import login api
from login import *
# import dashboard api
from dashboard import *
# import gameplay api
from gameplay import *

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
