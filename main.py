from flask import Flask, redirect, url_for, request, jsonify, Response
from flask_mysqldb import MySQL
import json
import os

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')

app.config['MYSQL_HOST'] = 'dcrhg4kh56j13bnu.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'rpawh9q7q2ra0ces'
app.config['MYSQL_PASSWORD'] = 'vurbee05mr0v4lgs'
app.config['MYSQL_DB'] = 'jxxv8laq46soz2mq'

mysql = MySQL(app)


@app.route('/success/<name>')
def success(name):
    # Creating a connection cursor
    cursor = mysql.connection.cursor()

    # Executing SQL Statements
    # cursor.execute(''' CREATE TABLE table_name(field1, field2...) ''')
    # cursor.execute(''' INSERT INTO table_name VALUES(v1,v2...) ''')
    # cursor.execute(''' DELETE FROM table_name WHERE condition ''')

    # Saving the Actions performed on the DB
    mysql.connection.commit()

    # Closing the cursor
    cursor.close()

    return json.dumps({'success': True, 'data': [{"name": "123"}]})


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

        if errorMsg == '':
            json_data = [dict(zip(row_headers, user))]
            return json.dumps({'success': True, 'data': [json_data]}, indent=4)
        else:
            return json.dumps({'success': False, 'errorMsg': errorMsg}, indent=4)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
