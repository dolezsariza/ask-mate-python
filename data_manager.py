from flask import Flask, request, redirect, render_template, url_for

import connection

def add_new_question():
    return connection.append_file("sample_data/question.csv", data_list, connection.QUESTION_HEADERS)
    # data_list is the submit dictionary

def add_new_answer():
    return connection.append_file("sample_data/answer.csv", data_list, connection.ANSWER_HEADERS)


def read_data(file):

    list_of_dicts = connection.read_file(file)
    sorted_list_of_dicts = sorted(list_of_dicts, key=lambda k: k['submission_time'],reverse=True)

    return sorted_list_of_dicts
