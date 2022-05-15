from flask import request, session, make_response, redirect

from main import app, mysql

@app.route('/getCurrentQuizTitle', methods=['POST','GET'])
def getCurrentQuizTitle():
    errorMsg = ''  # output error message if error occurred
    result = {}
    if request.method == 'GET':
        args = request.args
        quizId = args['quizid']
        user = session['user']
        studentId = user['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT UserQuiz.quiz_id,quiz_name, quiz_status, quiz_score, current_progress, score, status, subject_name "
                       "from UserQuiz, Quiz, Subject "
                       "where UserQuiz.quiz_id = Quiz.quiz_id "
                       "and Quiz.subject_id = Subject.subject_id "
                       "and user_id = %s and UserQuiz.quiz_id = %s", (str(studentId), str(quizId)))
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