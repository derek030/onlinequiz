from flask import request, session, make_response, redirect

from main import app, mysql

# Author: Chun Hin Chan(103846278)


from hashlib import sha256

import re

# Regular expression for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def check(email):
    # check email with regex
    if re.fullmatch(regex, email):
        return True
    else:
        return False

def hash_password(password):
    # returns the hashed version of a string
    return sha256(password.encode('utf-8')).hexdigest()

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
        print(sha256(userpassword.encode('utf-8')).hexdigest())
        if check(useremail):        # valid email format
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT user_id, user_name, user_type FROM User "
                           "WHERE email = %s AND  hashed_pwd = %s",
                           (useremail, hash_password(userpassword)))
            # Fetch one record and return result
            user = cursor.fetchone()
            if user is None:  # user not exist
                errorMsg = 'You have entered an invalid email or password!!!'
            else:
                session['user'] = user
            # Saving the Actions performed on the DB
            mysql.connection.commit()

            # Closing the cursor
            cursor.close()

            result["success"] = True if errorMsg == '' else False
            result["errorMsg"] = errorMsg
            result["data"] = user
        else:
            errorMsg = 'You have entered an invalid email format!!!'
            result["success"] = True if errorMsg == '' else False
            result["errorMsg"] = errorMsg
            result["data"] = ""

        res = make_response(result)
        if isRememberme:
            # cookie
            res.set_cookie("email", value=str(useremail))
        else:
            res.set_cookie("email", value="", expires=0)
        return res


@app.route('/logout', methods=['POST'])
def logout():
    errorMsg = ''  # output error message if error occurred
    result = {}
    # remove the user from the session if it is there
    if 'user' in session:
        session.pop('user', None)

    result["success"] = True if errorMsg == '' else False
    result["errorMsg"] = errorMsg
    result["data"] = ''
    res = make_response(result)

    return res
