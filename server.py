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

        data_manager.rewrite_file(question_id,'sample_data/question.csv', list_of_questions, 'question')

    questions = data_manager.get_question(question_id, data_manager.unix_to_utc(list_of_questions), "id")[0]

    list_of_answers = data_manager.read_data("sample_data/answer.csv")
    answers = data_manager.get_question(question_id, data_manager.unix_to_utc(list_of_answers), "question_id")


    return render_template('question.html', question=questions, answers=answers)


@app.route('/add-question', methods=["GET", 'POST'])
def route_add_question():
    if request.method == 'POST':
        data_manager.add_new_question(request.form)
        return redirect('/')

    return render_template('add-question.html')

@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    list_of_questions = data_manager.read_data("sample_data/question.csv")
    data_manager.delete_item(list_of_questions,question_id,"sample_data/question.csv","question")
    return redirect("/")

@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def post_answer(question_id):
    if request.method == 'POST':
        data_manager.add_new_answer(request.form)
        return redirect('/question/' + question_id)

    return render_template('add-answer.html', question_id=question_id)

"""
@app.route('/answer/<answer_id>/delete')
def delete_answer(id_):

    return redirect("/")
"""

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )

