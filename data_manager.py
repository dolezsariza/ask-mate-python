from datetime import datetime
import connection


def add_new_question(request_form):
    new_question = {'id': 12, 'submission_time': 1493368154, 'view_number': 0, 'vote_number': 0,
                    'title': str(request_form['title']), 'message': str(request_form['message']), 'image': None}
    return connection.append_file("sample_data/question.csv", new_question, connection.QUESTION_HEADERS)
    # data_list is the submit dictionary


def add_new_answer(data_list):
    return connection.append_file("sample_data/answer.csv", data_list, connection.ANSWER_HEADERS)


def read_data(file):

    list_of_dicts = connection.read_file(file)
    sorted_list_of_dicts = sorted(list_of_dicts, key=lambda k: k['submission_time'],reverse=True)

    return sorted_list_of_dicts


def unix_to_utc(list_of_dict):
    for dict in list_of_dict:
        dict["submission_time"] = datetime.utcfromtimestamp(int(dict["submission_time"])).strftime('%Y.%m.%d. %H:%M:%S')
    return list_of_dict


def get_question(id, list_of_dicts, id_type):
    data = []
    for item in list_of_dicts:
        if id == item[id_type]:
            data.append(item)
    return data
