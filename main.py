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

    return {"name": "123"}


@app.route('/login', methods=['POST', 'GET'])
def login():
    # print("122")
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
