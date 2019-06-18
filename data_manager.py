from datetime import datetime
from time import time
from psycopg2 import sql

import connection
@connection.connection_handler
def add_new_answer_SQL(cursor,message,question_id):
    cursor.execute("""
                   INSERT INTO answer(message,question_id) VALUES (%(message)s,%(question_id)s);
                   """,
                   {'message':message,'question_id':question_id})
# %(id)s,%(submission_time)s,%(vote_number)s, %(question_id)s
# 'id':id,'submission_time':submission_time,'vote_number':vote_number, 'question_id':question_id,'

@connection.connection_handler
def add_new_question_SQL(cursor,title,message):
    cursor.execute("""
                       INSERT INTO question(title, message) VALUES (%(title)s,%(message)s);
                       """,
                   {'title': title, 'message': message})

@connection.connection_handler
def get_question_by_id(cursor,question_id):
    cursor.execute("""
                    SELECT * from question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id':question_id})

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
def delete_question(cursor,question_id):
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id':question_id})


def delete_item(data_list,question_id,file,type):
    for dict in data_list:
        if dict["id"] == question_id:
            data_list.remove(dict)
    if type=="question":
        connection.write_file(file, data_list, connection.QUESTION_HEADERS)
    elif type=="answer":
        connection.write_file(file,data_list,connection.ANSWER_HEADERS)

"""

def add_new_question(request_form):
    new_question = {'id': generate_new_id('sample_data/question.csv'), 'submission_time': int(time()+7200),
                    'view_number': 0, 'vote_number': 0, 'title': str(request_form['title']),
                    'message': str(request_form['message']), 'image': None}
    return connection.append_file("sample_data/question.csv", new_question, connection.QUESTION_HEADERS)
    # data_list is the submit dictionary


def add_new_answer(request_form):
    new_answer = {'id': generate_new_id('sample_data/answer.csv'), 'submission_time': int(time()+7200),
                  'vote_number': 0, 'question_id': request_form['question_id'],
                  'message': str(request_form['message']), 'image': None}
    return connection.append_file("sample_data/answer.csv", new_answer, connection.ANSWER_HEADERS)

"""
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


def rewrite_file(id_, file, data_list, headers):
    if headers == 'question':
        headers = connection.QUESTION_HEADERS
        question = get_question_or_answers(id_, data_list, "id")[0]
        question['view_number'] = int(question['view_number'])
        question['view_number'] += 1
    elif headers == 'answer':
        headers = connection.ANSWER_HEADERS

    connection.write_file(file, data_list, headers)

def delete_item(data_list,question_id,file,type):
    for dict in data_list:
        if dict["id"] == question_id:
            data_list.remove(dict)
    if type=="question":
        connection.write_file(file, data_list, connection.QUESTION_HEADERS)
    elif type=="answer":
        connection.write_file(file,data_list,connection.ANSWER_HEADERS)