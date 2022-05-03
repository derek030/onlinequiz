from flask import request, session, make_response, redirect

from main import app, mysql

badgelevel = {'beginner': 0, 'bronze': 50, 'silver': 100, 'gold': 500, 'platinum': 1000}

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
    if request.method == 'GET':
        user = session['user']
        studentId = user['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT score "
                       "from UserQuiz "
                       "where user_id = %s", str(studentId))
        # Fetch records and return result
        scorelist = cursor.fetchall()
        print(scorelist)
        print(len(scorelist))
        # Saving the Actions performed on the DB
        mysql.connection.commit()
        # Closing the cursor
        cursor.close()
        # sum up all the score from the quiz
        if len(scorelist) > 0:
            for score in scorelist:
                total += score['score']
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
        result["data"] = {'current_score': total, 'current_badge': badge, "next_badge": nextbadge, "next_badge_score": nextbadgescore}
        res = make_response(result)

        return res