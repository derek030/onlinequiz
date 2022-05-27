# Author: Chun Hin Chan(103846278)
# all api related to dashboard (student and tutor) function

from flask import request, session, make_response, redirect

from main import app, mysql

# Badge level
badgelevel = {'bronze': 0, 'silver': 200, 'gold': 500, 'platinum': 1000, 'diamond': 2000}


# get quiz list api
@app.route('/getQuizList', methods=['GET'])
def getQuizList():
    errorMsg = ''  # output error message if error occurred
    result = {}
    if request.method == 'GET':
        # args = request.args
        user = session['user']
        userId = user['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT UserQuiz.quiz_id,quiz_name, quiz_status, quiz_score, current_progress, score, status, subject_name "
            "from UserQuiz, Quiz, Subject "
            "where UserQuiz.quiz_id = Quiz.quiz_id "
            "and Quiz.subject_id = Subject.subject_id "
            "and user_id = %s", str(userId))
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


# get student score api
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
        result["data"] = {'current_score': total, 'current_badge': badge, "next_badge": nextbadge,
                          "next_badge_score": nextbadgescore, "completed": completedcount}
        res = make_response(result)

        return res


# get leaderboard information api
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


# update quiz status api
@app.route('/updateQuizStatus', methods=['GET'])
def updateQuizStatus():
    errorMsg = ''  # output error message if error occurred
    result = {}
    if request.method == 'GET':
        args = request.args
        print(args)
        qid = args['qid']
        currentStatus = args['currentStatus']
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE Quiz "
                       "SET quiz_status = %s WHERE quiz_id = %s;",
                       (str(currentStatus), qid))
        rows_affected = cursor.rowcount
        if rows_affected == 0:
            errorMsg = "Nothing Updated"
        # Saving the Actions performed on the DB
        mysql.connection.commit()
        # Closing the cursor
        cursor.close()

        result["success"] = True if errorMsg == '' else False
        result["errorMsg"] = errorMsg
        result["data"] = ""
        res = make_response(result)

        return res


# get enrolled subject api
@app.route('/getEnrolledSubject', methods=['GET'])
def getEnrolledSubject():
    errorMsg = ''  # output error message if error occurred
    result = {}
    if request.method == 'GET':
        user = session['user']
        userId = user['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT UserSubject.user_id, user_name, user_type, UserSubject.subject_id, subject_name "
                       "FROM UserSubject, User, Subject "
                       "WHERE UserSubject.user_id = User.user_id "
                       "AND UserSubject.subject_id = Subject.subject_id "
                       "AND User.user_id = %s ", str(userId))
        # Fetch records and return result
        recordlist = cursor.fetchall()
        print(recordlist)
        # Saving the Actions performed on the DB
        mysql.connection.commit()
        # Closing the cursor
        cursor.close()

        result["success"] = True if errorMsg == '' else False
        result["errorMsg"] = errorMsg
        result["data"] = recordlist
        res = make_response(result)

        return res


# get subject's student result api
@app.route('/getSubjectStudentResults', methods=['GET'])
def getSubjectStudentResults():
    errorMsg = ''  # output error message if error occurred
    result = {}
    if request.method == 'GET':
        args = request.args
        target = args['subjectid']
        print(target)
        subject_ids = target.split(", ")
        print(subject_ids)
        print(tuple(subject_ids))
        if len(subject_ids) > 1:
            query = 'SELECT Quiz.subject_id, subject_name, user_name ' \
                    'FROM UserQuiz, User, Quiz, Subject, UserSubject ' \
                    'WHERE UserQuiz.user_id = User.user_id ' \
                    'AND UserQuiz.quiz_id = Quiz.quiz_id ' \
                    'AND Quiz.subject_id = Subject.subject_id ' \
                    'AND UserSubject.user_id = User.user_id ' \
                    'AND UserSubject.subject_id = Subject.subject_id ' \
                    'AND user_type = \'student\' AND status = \'completed\' ' \
                    'AND Quiz.subject_id IN {} '.format(tuple(subject_ids))
        else:
            query = 'SELECT Quiz.subject_id, subject_name, user_name ' \
                    'FROM UserQuiz, User, Quiz, Subject, UserSubject ' \
                    'WHERE UserQuiz.user_id = User.user_id ' \
                    'AND UserQuiz.quiz_id = Quiz.quiz_id ' \
                    'AND Quiz.subject_id = Subject.subject_id ' \
                    'AND UserSubject.user_id = User.user_id ' \
                    'AND UserSubject.subject_id = Subject.subject_id ' \
                    'AND user_type = \'student\' AND status = \'completed\' ' \
                    'AND Quiz.subject_id = {} '.format(str(target))
        print(query)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        # Fetch records and return result
        recordlist = cursor.fetchall()
        print(recordlist)
        # Saving the Actions performed on the DB
        mysql.connection.commit()
        # Closing the cursor
        cursor.close()

        result["success"] = True if errorMsg == '' else False
        result["errorMsg"] = errorMsg
        result["data"] = recordlist
        res = make_response(result)

        return res
