from flask import Flask, request, redirect, render_template, url_for

import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    return render_template('list.html')


@app.route('/question/<question_id>')
def route_question(question_id):
    return render_template('question.html', question=question)


@app.route('/add-question', methods=["GET", 'POST'])
def route_add_question():
    return render_template('add-question.thml')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )