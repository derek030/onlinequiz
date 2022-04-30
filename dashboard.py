from flask import request, session, make_response, redirect

from main import app, mysql


@app.route('/getQuizList', methods=['GET'])
def getQuizList():
    errorMsg = ''  # output error message if error occurred
    result = {}
    if request.method == 'GET':
        args = request.args
        print(args)     # For debugging
        studentId = args['studentID']
        print(studentId)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT UserQuiz.quiz_id,quiz_name, quiz_status, current_progress, score, status, subject_name "
                       "from UserQuiz, Quiz, Subject "
                       "where UserQuiz.quiz_id = Quiz.quiz_id "
                       "and Quiz.subject_id = Subject.subject_id "
                       "and user_id = %s", studentId)
        # Fetch records and return result
        quizList = cursor.fetchall()
        print(quizList)
        print(len(quizList))
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
