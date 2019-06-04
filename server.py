from flask import Flask, request, redirect, render_template, url_for

import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    list_of_questions = data_manager.read_data("sample_data/question.csv")
    questions = data_manager.unix_to_utc(list_of_questions)

    return render_template('list.html',questions=questions)


@app.route('/question')
def route_question():
    return render_template('question.html')


@app.route('/add-question')
def route_add_question():
    return render_template('add-question.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )

