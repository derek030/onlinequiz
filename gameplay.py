# Author: Chun Hin Chan(103846278)
# all api related to quiz game play function

from flask import request, session, make_response, redirect

from main import app, mysql


# get quiz title api
@app.route('/getCurrentQuizTitle', methods=['POST', 'GET'])
def getCurrentQuizTitle():
    errorMsg = ''  # output error message if error occurred
    result = {}
    if request.method == 'GET':
        args = request.args
        quizId = args['quizid']
        user = session['user']
        studentId = user['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT UserQuiz.quiz_id, quiz_name, quiz_status, quiz_score, current_progress, score, status, subject_name "
            "from UserQuiz, Quiz, Subject "
            "where UserQuiz.quiz_id = Quiz.quiz_id "
            "and Quiz.subject_id = Subject.subject_id "
            "and user_id = %s and UserQuiz.quiz_id = %s", (str(studentId), str(quizId)))
        # Fetch records and return result
        quizList = cursor.fetchall()
        if len(quizList) == 0:  # cannot find quiz
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


# get question list api
@app.route('/getQuestionList', methods=['POST', 'GET'])
def getQuestionList():
    errorMsg = ''  # output error message if error occurred
    result = {}
    if request.method == 'GET':
        args = request.args
        quizId = args['quizid']
        user = session['user']
        studentId = user['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT  user_quiz_question_id, UserQuizQuestion.user_quiz_id , user_id, UserQuizQuestion.question_id, question, option_a, option_b, option_c, option_d, correct_answer, quiz_score "
            "FROM UserQuiz, UserQuizQuestion, Question, Quiz "
            "WHERE UserQuiz.user_quiz_id = UserQuizQuestion.user_quiz_id "
            "AND UserQuizQuestion.question_id = Question.question_id "
            "AND UserQuiz.quiz_id = Quiz.quiz_id "
            "AND user_id = %s AND UserQuiz.quiz_id = %s;", (str(studentId), str(quizId)))
        # Fetch records and return result
        questionsList = cursor.fetchall()
        if len(questionsList) == 0:  # quiz don't have any question
            errorMsg = 'questionsList is empty'
        # Saving the Actions performed on the DB
        mysql.connection.commit()
        # Closing the cursor
        cursor.close()

        result["success"] = True if errorMsg == '' else False
        result["errorMsg"] = errorMsg
        result["data"] = questionsList
        res = make_response(result)

        return res


# update user quiz status api
@app.route('/updateUserQuizStatus', methods=['POST', 'GET'])
def updateUserQuizStatus():
    errorMsg = ''  # output error message if error occurred
    result = {}
    if request.method == 'GET':
        args = request.args
        print(args)
        uqqid = args['uqqid']
        uqid = args['uqid']
        questionid = args['questionid']
        answer = args['answer']
        isCorrect = args['isCorrect']
        currentprogress = args['currentprogress']
        totalmark = args['totalmark']
        currentStatus = args['currentStatus']

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE UserQuizQuestion "
                       "SET user_answer =  %s, is_correct = %s WHERE user_quiz_question_id = %s AND question_id = %s;",
                       (str(answer), isCorrect, uqqid, questionid))

        cursor.execute("UPDATE UserQuiz "
                       "SET current_progress =  %s, score = %s, status = %s WHERE user_quiz_id = %s;",
                       (currentprogress, totalmark, currentStatus, uqid))

        # Saving the Actions performed on the DB
        mysql.connection.commit()
        # Closing the cursor
        cursor.close()

        result["success"] = True if errorMsg == '' else False
        result["errorMsg"] = errorMsg
        result["data"] = ""
        res = make_response(result)

        return res


# get user quiz result api
@app.route('/getQuizResult', methods=['POST', 'GET'])
def getQuizResult():
    errorMsg = ''  # output error message if error occurred
    result = {}
    if request.method == 'GET':
        args = request.args
        quizId = args['quizid']
        user = session['user']
        studentId = user['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT user_id, quiz_id, score, current_progress, status, sum(is_correct) as correctcount "
                       "FROM UserQuiz, UserQuizQuestion "
                       "WHERE UserQuiz.user_quiz_id = UserQuizQuestion.user_quiz_id "
                       "AND user_id = %s and quiz_id = %s", (str(studentId), str(quizId)))
        # Fetch records and return result
        record = cursor.fetchall()
        if len(record) == 0:  # cannot find quiz record
            errorMsg = 'record not found'
        # Saving the Actions performed on the DB
        mysql.connection.commit()
        # Closing the cursor
        cursor.close()

        result["success"] = True if errorMsg == '' else False
        result["errorMsg"] = errorMsg
        result["data"] = record
        res = make_response(result)

        return res
