from flask import Flask, request, redirect, render_template, url_for

import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    list_of_questions = data_manager.read_data("sample_data/question.csv")
    questions = data_manager.unix_to_utc(list_of_questions)

    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>', methods=['GET'])
def route_question(question_id):

    list_of_questions = data_manager.read_data("sample_data/question.csv")
    if request.method == 'GET':
        question = data_manager.get_question(question_id, list_of_questions, "id")[0]
        question['view_number'] = int(question['view_number'])
        question['view_number'] += 1
        data_manager.rewrite_file('sample_data/question.csv', list_of_questions, 'question')
    questions = data_manager.unix_to_utc(list_of_questions)
    question = data_manager.get_question(question_id, questions,"id")[0]
    list_of_answers = data_manager.read_data("sample_data/answer.csv")
    answers = data_manager.get_question(question_id,list_of_answers,"question_id")
    answers_utc = data_manager.unix_to_utc(answers)





    return render_template('question.html', question=question, answers=answers_utc)


@app.route('/add-question', methods=["GET", 'POST'])
def route_add_question():
    if request.method == 'POST':
        data_manager.add_new_question(request.form)
        return redirect('/')

    return render_template('add-question.html')


# @app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
# def post_answer(question_id):
#     if request.method == 'POST':
#
#
#     return render_template('add-answer.html')



if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )

