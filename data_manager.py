from datetime import datetime
from psycopg2 import sql

import connection


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
def add_new_question_SQL(cursor,title,message):
    submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
                       INSERT INTO question(title, message, submission_time, view_number, vote_number) 
                       VALUES (%(title)s,%(message)s,%(submission_time)s, 0, 0);
                       """,
                   {'title': title, 'message': message, 'submission_time': submission_time})

@connection.connection_handler
def edit_question_SQL(cursor,title,message,question_id):
    cursor.execute("""
                    UPDATE question
                    SET title = %(title)s, message = %(message)s
                    WHERE id = %(question_id)s;
                    """,
                   {'title': title, 'message': message, 'question_id': question_id})



@connection.connection_handler
def add_new_answer_SQL(cursor,message,question_id):
    submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
                   INSERT INTO answer(message,question_id,vote_number,submission_time) 
                   VALUES (%(message)s,%(question_id)s, 0, %(submission_time)s);
                   """,
                   {'message': message,'question_id': question_id, 'submission_time': submission_time})

@connection.connection_handler
def add_new_comment_to_question(cursor,message,question_id):
    submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
                    INSERT INTO comment(question_id,message,submission_time) VALUES (%(question_id)s,%(message)s,%(submission_time)s)
                    """,
                   {'question_id':question_id,'message':message,'submission_time':submission_time})

@connection.connection_handler
def add_new_comment_to_answer(cursor,message,answer_id):
    submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
                    INSERT INTO comment(answer_id,message,submission_time) VALUES (%(answer_id)s,%(message)s,%(submission_time)s)
                    """,
                   {'answer_id':answer_id,'message':message,'submission_time':submission_time})

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


# innentől még CSV
def read_data(file):

    list_of_dicts = connection.read_file(file)
    sorted_list_of_dicts = sorted(list_of_dicts, key=lambda k: k['submission_time'], reverse=True)

    return sorted_list_of_dicts


def unix_to_utc(list_of_dict):
    for dict_ in list_of_dict:
        dict_["submission_time"] = datetime.utcfromtimestamp(int(dict_["submission_time"])).strftime('%Y.%m.%d. %H:%M:%S')
    return list_of_dict


def get_question_or_answers(id_, list_of_dicts, id_type):
    data = []
    for item in list_of_dicts:
        if id_ == item[id_type]:
            data.append(item)
    return data


def generate_new_id(file_path):
    length_of_file = len(read_data(file_path))
    id_ = length_of_file
    return id_


@connection.connection_handler
def raise_views_number(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET view_number = view_number + 1
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