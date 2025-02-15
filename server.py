from flask import Flask, request, redirect, render_template, url_for, session

import data_manager

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]iza/'


def login_required(func, **kwargs):
    def wrapper(**kwargs):
        try:
            temp = session['username']
        except KeyError:
            return render_template('denied.html')
        return func(**kwargs)
    return wrapper


@app.route('/index')
@login_required
def main():
    username = session['username']
    questions = data_manager.show_latest_questions()
    return render_template('list.html',questions=questions, username=username)


@app.route('/list', endpoint='route_list')
@login_required
def route_list():
    username = session['username']
    questions = data_manager.read_questions()
    return render_template('list.html', questions=questions, username=username)


@app.route('/question/<question_id>', methods=["GET"], endpoint='route_question')
@login_required
def route_question(question_id):
    data_manager.raise_views_number(question_id)
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.read_answers(question_id)
    comments_q = data_manager.read_comments_question(question_id)
    answer_ids = data_manager.get_answer_ids(question_id)

    comments_a = []
    for answer_id in answer_ids:
        for value in answer_id:
            new = answer_id[value]
            comments_a.append(data_manager.get_comments_by_answer_id(new))

    return render_template('question.html',
                           question=question,
                           answers=answers,
                           comments_q=comments_q,
                           comments_a=comments_a,
                           username = session['username'])

@app.route('/add-question', methods=["GET", 'POST'], endpoint='route_add_question')
@login_required
def route_add_question():
    username = session['username']
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        username = session['username']
        data_manager.add_new_question_SQL(title,message,username)
        return redirect('/index')

    return render_template('add-question.html', username=username)


@app.route('/question/<question_id>/edit-question', methods=["GET", "POST"], endpoint='edit_question')
@login_required
def edit_question(question_id):
    username = session['username']
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        data_manager.edit_question_SQL(title, message, question_id)
        return redirect('/index')

    title_original = 0
    edit_title_data = data_manager.get_edit_title(question_id)
    for data in edit_title_data:
        for value in data:
            title_original = data[value]
    message_original = 0
    edit_message_data = data_manager.get_edit_message(question_id)
    for data in edit_message_data:
        for value in data:
            message_original = data[value]

    return render_template('edit-question.html', question_id = question_id, title_original = title_original, message_original = message_original, username=username)

@app.route('/answer/<answer_id>/edit-answer', methods=["GET", "POST"], endpoint='edit_answer')
@login_required
def edit_answer(answer_id):
    username = session['username']
    if request.method == 'POST':
        message = request.form['message']
        data_manager.edit_answer_SQL(message, answer_id)
        return redirect('/index')

    message_original = 0
    edit_message_data = data_manager.get_edit_message_answer(answer_id)
    for data in edit_message_data:
        for value in data:
            message_original = data[value]

    return render_template('edit-answer.html', answer_id = answer_id, message_original = message_original, username=username)

@app.route('/comment/<comment_id>/edit-comment', methods=["GET", "POST"], endpoint='edit_comment')
@login_required
def edit_comment(comment_id):
    username = session['username']
    if request.method == 'POST':
        message = request.form['message']
        data_manager.edit_comment_SQL(message, comment_id)
        return redirect('/index')

    message_original = 0
    edit_message_data = data_manager.get_edit_comment(comment_id)
    for data in edit_message_data:
        for value in data:
            message_original = data[value]

    return render_template('edit_comment.html', comment_id = comment_id, message_original = message_original, username=username)


@app.route('/question/<question_id>/delete', endpoint='delete_question')
@login_required
def delete_question(question_id):
    answer_ids = data_manager.get_answer_ids(question_id)
    if len(answer_ids) != 0:
        for answer_id in answer_ids:
            for value in answer_id:
                new = answer_id[value]
                data_manager.delete('comment', 'answer_id', new)

    data_manager.delete('comment','question_id',question_id)
    data_manager.delete('answer','question_id',question_id)
    data_manager.delete('question','id',question_id)
    return redirect("/index")


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'], endpoint='post_answer')
@login_required
def post_answer(question_id):
    username = session['username']
    if request.method == 'POST':
        message=request.form['message']
        username = session['username']
        data_manager.add_new_answer_SQL(message,question_id,username)
        return redirect(url_for('route_question', question_id=question_id))
    return render_template('add-answer.html',question_id=question_id, username=username)


@app.route('/answer/<answer_id>/delete', endpoint='delete_answer')
@login_required
def delete_answer(answer_id):
    data_manager.delete('comment', 'answer_id', answer_id)
    data_manager.delete('comment','answer_id',answer_id)
    data_manager.delete('answer','id',answer_id)
    return redirect("/index")

@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'], endpoint='post_comment_to_question')
@login_required
def post_comment_to_question(question_id):
    username = session['username']
    if request.method == 'POST':
        message=request.form['message']
        username = session['username']
        data_manager.add_new_comment_to_question(message,question_id,username)
        return redirect(url_for('route_question', question_id=question_id))

    return render_template('add-comment-q.html', question_id=question_id, username=username)

@app.route('/comments/<comment_id>/delete', endpoint='delete_comment')
@login_required
def delete_comment(comment_id):
    data_manager.delete('comment','id',comment_id)

    return redirect("/index")


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'], endpoint='post_comment_to_answer')
@login_required
def post_comment_to_answer(answer_id):
    username = session['username']
    if request.method == 'POST':
        message=request.form['message']
        username = session['username']
        data_manager.add_new_comment_to_answer(message,answer_id,username)
        return redirect("/index")

    return render_template('add-comment-a.html', answer_id=answer_id, username=username)



@app.route('/question/<question_id>/vote/up', endpoint='vote_up_question')
@login_required
def vote_up_question(question_id):
    data_manager.up_vote_question(question_id)
    data_manager.decrease_views_number(question_id)
    return redirect(url_for('route_question', question_id=question_id))


@app.route('/question/<question_id>/vote/down', endpoint='vote_down_question')
@login_required
def vote_down_question(question_id):
    data_manager.down_vote_question(question_id)
    data_manager.decrease_views_number(question_id)
    return redirect(url_for('route_question', question_id=question_id))


#visibility line for new FUNKtions

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hash = data_manager.get_user_hash(username)[0]['password']
        access = data_manager.verify_password(password, hash)
        if access == True:
            session['username'] = request.form['username']
            return redirect('/index')
        if access == False:
            return render_template('denied.html')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = data_manager.hash_password(request.form['password'])
        email = request.form['email']
        data_manager.add_user(username, password, email)
        return redirect('/login')

    return render_template('register.html')


@app.route("/users", endpoint='list_all_users')
@login_required
def list_all_users():
    username = session['username']
    users = data_manager.get_users()

    return render_template('users.html',users=users, username=username)

@app.route("/users/<username>", endpoint="show_user_data")
@login_required
def show_user_data(username):
    #username = session['username']
    user_data = data_manager.get_user_data(username)
    user_questions = data_manager.get_user_questions(username)
    user_answers = data_manager.get_user_answers(username)
    user_comments = data_manager.get_user_comments(username)
    return render_template('user_data.html',
                           user_data=user_data,
                           user_questions=user_questions,
                           user_answers=user_answers,
                           user_comments=user_comments,
                           username=username)



if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=9000,
        debug=True,
    )

