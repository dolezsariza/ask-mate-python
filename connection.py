import os
import psycopg2
import psycopg2.extras

import csv

ANSWER_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", 'image']
QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWERS_CSV = "sample_data/answer.csv"
QUESTION_CSV = "sample_data/question.csv"
# dictahed = ["idea","new","next"]
# dicta = {"idea": "meh", "new":"level","next":"shit"}


def read_file(file):
    with open(file, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        data_from_file = [dict(story) for story in reader]

    return data_from_file


def write_file(file, data_list, fieldnames):
    with open(file, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for dictionary in data_list:
            writer.writerow(dictionary)


def unix_to_utc(list_of_dict):
    for dict_ in list_of_dict:
        dict_["submission_time"] = datetime.utcfromtimestamp(int(dict_["submission_time"])).strftime('%Y.%m.%d. %H:%M:%S')
    return list_of_dict

def append_file(file, data_list, fieldnames):
    with open(file, "a") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow(data_list)

"""
new = read_file("sample_data/question.csv")
print(new)

for row in new:
    for key,value in row.items():
        print(f'{key}:{value}')
"""


def get_connection_string():
    # setup connection string
    # to do this, please define these environment variables first
    user_name = os.environ.get('PSQL_USER_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    database_name = os.environ.get('PSQL_DB_NAME')

    env_variables_defined = user_name and password and host and database_name

    if env_variables_defined:
        # this string describes all info for psycopg2 to connect to the database
        return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')


def open_database():
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a RealDictCursor cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value

    return wrapper