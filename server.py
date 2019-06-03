from flask import Flask, request, redirect, render_template, url_for

app = Flask


@app.route('/')
@app.route('/list')
def route_list():
    return render_template('list.html')


@app.route('/question')
def route_question():
    return render_template('question.html')


@app.route('/add-question')
def route_add_question():
    return render_template('add-question.thml')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )