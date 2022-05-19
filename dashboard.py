from flask import request, session, make_response, redirect

from main import app, mysql

badgelevel = {'bronze': 0, 'silver': 200, 'gold': 500, 'platinum': 1000, 'diamond': 2000}

@app.route('/getQuizList', methods=['GET'])
def getQuizList():
    errorMsg = ''  # output error message if error occurred
    result = {}
    if request.method == 'GET':
        #args = request.args
        user = session['user']
        studentId = user['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT UserQuiz.quiz_id,quiz_name, quiz_status, quiz_score, current_progress, score, status, subject_name "
                       "from UserQuiz, Quiz, Subject "
                       "where UserQuiz.quiz_id = Quiz.quiz_id "
                       "and Quiz.subject_id = Subject.subject_id "
                       "and user_id = %s", str(studentId))
        # Fetch records and return result
        quizList = cursor.fetchall()
        if len(quizList) == 0:  # user does not have quiz
            errorMsg = 'quizList is empty'
        # Saving the Actions performed on the DB
        mysql.connection.commit()
        # Closing the cursor
        cursor.close()

        result["success"] = True if errorMsg == '' else False
        result["errorMsg"] = errorMsg
        result["data"] = quizList
        res = make_response(result)

        return res


@app.route('/getScore', methods=['GET'])
def getScore():
    errorMsg = ''  # output error message if error occurred
    result = {}
    total = 0
    badge = ''
    nextbadge = ''
    nextbadgescore = 0
    completedcount = 0
    if request.method == 'GET':
        user = session['user']
        studentId = user['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT CAST(SUM(score) AS SIGNED) total, COUNT(status) AS completed "
                       "FROM UserQuiz "
                       "WHERE user_id = %s AND status = 'completed'", str(studentId))
        # Fetch records and return result
        record = cursor.fetchone()
        print(record)
        # Saving the Actions performed on the DB
        mysql.connection.commit()
        # Closing the cursor
        cursor.close()
        # get completed count and total score
        total = record['total']
        if total is None:
            total = 0
        completedcount = record['completed']
        # find the current badge level according to the user's total score
        for key, value in badgelevel.items():
            if total >= value:
                badge = key
            else:
                nextbadge = key
                nextbadgescore = value
                break
        print(nextbadge)
        result["success"] = True if errorMsg == '' else False
        result["errorMsg"] = errorMsg
        result["data"] = {'current_score': total, 'current_badge': badge, "next_badge": nextbadge, "next_badge_score": nextbadgescore, "completed": completedcount}
        res = make_response(result)

        return res

@app.route('/getLeaderboard', methods=['GET'])
def getLeaderboard():
    errorMsg = ''  # output error message if error occurred
    result = {}
    if request.method == 'GET':
        user = session['user']
        studentId = user['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT User.user_id, user_name, CAST(SUM(score) AS SIGNED) total "
                       "FROM User, UserQuiz "
                       "WHERE User.user_id = UserQuiz.user_id "
                       "AND user_type = 'student'"
                       "GROUP BY User.user_id "
                       "ORDER BY total DESC")
        # Fetch records and return result
        recordlist = cursor.fetchall()
        print(recordlist)
        # Saving the Actions performed on the DB
        mysql.connection.commit()
        # Closing the cursor
        cursor.close()
        # get top five records
        top5records = []
        for record in recordlist:
            if len(top5records) < 5:
                top5records.append(record)
        print(top5records)
        result["success"] = True if errorMsg == '' else False
        result["errorMsg"] = errorMsg
        result["data"] = top5records
        res = make_response(result)

        return res