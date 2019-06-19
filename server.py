from flask import Flask, request, redirect, render_template, url_for

import data_manager

app = Flask(__name__)

@app.route('/')
@app.route('/list')
def route_list():
    questions = data_manager.read_questions()

    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>')
def route_question(question_id):

    question = data_manager.get_question_by_id(question_id)

    answers = data_manager.read_answers(question_id)

    return render_template('question.html', question=question, answers=answers)


@app.route('/add-question', methods=["GET", 'POST'])
def route_add_question():
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        data_manager.add_new_question_SQL(title,message)
        return redirect('/')

    return render_template('add-question.html')

@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete('comment','question_id',question_id)
    data_manager.delete('answer','question_id',question_id)
    data_manager.delete('question','id',question_id)
    return redirect("/")

@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def post_answer(question_id):
    if request.method == 'POST':
        message=request.form['message']
        data_manager.add_new_answer_SQL(message,question_id)
        return redirect(url_for('route_question', question_id=question_id))

    return render_template('add-answer.html',question_id=question_id)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    data_manager.delete('comment','answer_id',answer_id)
    data_manager.delete('answer','id',answer_id)

    return redirect("/")


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )

