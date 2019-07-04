from datetime import datetime
from psycopg2 import sql
import bcrypt

import connection


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@connection.connection_handler
def show_latest_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY submission_time DESC LIMIT 5
                    """)
    data = cursor.fetchall()
    return data

@connection.connection_handler
def get_question_by_id(cursor,question_id):
    cursor.execute("""
                    SELECT * from question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id':question_id})
    data = cursor.fetchall()
    return data[0]

@connection.connection_handler
def add_new_question_SQL(cursor,title,message, username):
    submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
                       INSERT INTO question(title, message, submission_time, view_number, vote_number, username, user_id) 
                       VALUES (%(title)s,%(message)s,%(submission_time)s, 0, 0, %(username)s,
                       (SELECT id FROM users WHERE username = %(username)s));
                       """,
                   {'title': title, 'message': message, 'submission_time': submission_time, 'username': username})

@connection.connection_handler
def edit_question_SQL(cursor,title,message,question_id):
    cursor.execute("""
                    UPDATE question
                    SET title = %(title)s, message = %(message)s
                    WHERE id = %(question_id)s;
                    """,
                   {'title': title, 'message': message, 'question_id': question_id})


@connection.connection_handler
def edit_answer_SQL(cursor,message,answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET message = %(message)s
                    WHERE id = %(answer_id)s;
                    """,
                   {'message': message, 'answer_id': answer_id})


@connection.connection_handler
def add_new_answer_SQL(cursor,message,question_id, username):
    submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
                   INSERT INTO answer(message,question_id,vote_number,submission_time, username, user_id) 
                   VALUES (%(message)s,%(question_id)s, 0, %(submission_time)s, %(username)s,
                   (SELECT id FROM users WHERE username = %(username)s));
                   """,
                   {'message': message,'question_id': question_id, 'submission_time': submission_time,'username':username})

@connection.connection_handler
def add_new_comment_to_question(cursor,message,question_id, username):
    submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
                    INSERT INTO comment(question_id,message,submission_time, username,user_id) 
                    VALUES (%(question_id)s,%(message)s,%(submission_time)s, %(username)s,
                    (SELECT id FROM users WHERE username = %(username)s));
                    """,
                   {'question_id':question_id,'message':message,'submission_time':submission_time,'username':username})

@connection.connection_handler
def add_new_comment_to_answer(cursor,message,answer_id, username):
    submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
                    INSERT INTO comment(answer_id,message,submission_time, username, user_id) 
                    VALUES (%(answer_id)s,%(message)s,%(submission_time)s, %(username)s,
                    (SELECT id FROM users WHERE username = %(username)s));
                    """,
                   {'answer_id':answer_id,'message':message,'submission_time':submission_time, 'username':username})

@connection.connection_handler
def read_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question;
                    """)
    data = cursor.fetchall()
    return data

@connection.connection_handler
def read_answers(cursor,question_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id=%(question_id)s;
                    """,
                   {'question_id':question_id})

    data = cursor.fetchall()
    return data

@connection.connection_handler
def read_comments_question(cursor,question_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE question_id=%(question_id)s;
                    """,
                   {'question_id':question_id})

    data = cursor.fetchall()
    return data

@connection.connection_handler
def read_comments_answer(cursor,answer_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE answer_id=%(answer_id)s;
                    """,
                   {'answer_id':answer_id})

    data = cursor.fetchall()
    return data


@connection.connection_handler
def delete(cursor, table, parameter, value):
    cursor.execute(sql.SQL("DELETE FROM {0} WHERE {1} = %s")
                   .format(sql.Identifier(table), sql.Identifier(parameter)), [value])


@connection.connection_handler
def up_vote_question(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = vote_number + 1
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})


@connection.connection_handler
def down_vote_question(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = vote_number - 1
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})


@connection.connection_handler
def up_vote_answer(cursor, answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number + 1
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id})

@connection.connection_handler
def down_vote_answer(cursor, answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number - 1
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id})


@connection.connection_handler
def get_edit_title(cursor, question_id):
    cursor.execute("""
                    SELECT title FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})

    data = cursor.fetchall()
    return data

@connection.connection_handler
def get_edit_message(cursor, question_id):
    cursor.execute("""
                    SELECT message FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})

    data = cursor.fetchall()
    return data

@connection.connection_handler
def get_edit_message_answer(cursor, answer_id):
    cursor.execute("""
                    SELECT message FROM answer
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id})

    data = cursor.fetchall()
    return data



@connection.connection_handler
def raise_views_number(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET view_number = view_number + 1
                    WHERE id = %(question_id)s;
                    
                    """,
                   {'question_id': question_id})


@connection.connection_handler
def decrease_views_number(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET view_number = view_number - 1
                    WHERE id = %(question_id)s;

                    """,
                   {'question_id': question_id})


@connection.connection_handler
def get_answer_ids(cursor,question_id):
    cursor.execute("""
                    SELECT id FROM answer
                    WHERE question_id=%(question_id)s;
                    """,
                   {'question_id':question_id})
    data = cursor.fetchall()
    return data

@connection.connection_handler
def get_comments_by_answer_id(cursor,answer_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE answer_id = %(answer_id)s;
                    """,
                   {'answer_id':answer_id})

    data = cursor.fetchall()
    return data


@connection.connection_handler
def get_users(cursor):
    cursor.execute("""
                    SELECT * FROM users
                    ORDER BY id;
                    """)

    data = cursor.fetchall()
    return data

@connection.connection_handler
def add_user(cursor, username, password, email):
    cursor.execute("""
                    INSERT INTO users(username, password, email) 
                    VALUES (%(username)s,%(password)s,%(email)s);
                   """,
                   {'username': username, 'password': password, 'email': email})


@connection.connection_handler
def get_user_hash(cursor, username):
    cursor.execute("""
                    SELECT password FROM users
                    WHERE username = %(username)s;
                    """,
                    {'username': username})

    data = cursor.fetchall()
    return data

@connection.connection_handler
def get_user_data(cursor, username):
    cursor.execute("""
                    SELECT id, username, email
                    FROM users

                    WHERE users.username = %(username)s;
                    """,
                   {'username': username})

    return cursor.fetchall()

@connection.connection_handler
def get_user_questions(cursor,username):
    cursor.execute("""
                    SELECT question.title AS title,
                    question.message AS message
                    FROM users
                    LEFT JOIN question
                    ON (users.id = question.user_id)
                   
                    WHERE users.username = %(username)s;
                    """,
                   {'username':username})

    return cursor.fetchall()


@connection.connection_handler
def get_user_answers(cursor, username):
    cursor.execute("""
                    SELECT answer.message AS a_message
                    FROM users
                    LEFT JOIN answer
                    ON (users.id = answer.user_id)

                    WHERE users.username = %(username)s;
                    """,
                   {'username': username})

    return cursor.fetchall()

@connection.connection_handler
def get_user_comments(cursor, username):
    cursor.execute("""
                    SELECT comment.message AS c_message
                    FROM users
                    LEFT JOIN comment
                    ON (users.id = comment.user_id)

                    WHERE users.username = %(username)s;
                    """,
                   {'username': username})

    return cursor.fetchall()
