from flask import request, session, make_response, redirect

from main import app, mysql


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
        cursor.execute("SELECT user_id, user_name, user_type FROM User WHERE email = %s AND  pwd = %s",
                       (useremail, userpassword))
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
