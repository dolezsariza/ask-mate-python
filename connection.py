from flask import Flask, request, redirect, render_template, url_for

import csv

ANSWER_HEADERS = ["id","submission_time","vote_number","question_id","message","image"]
QUESTION_HEADERS = ["id","submission_time","view_number","vote_number","title","message","image"]
ANSWERS_CSV = "sample_data/answer.csv"
QUESTION_CSV = "sample_data/question.csv"
# dictahed = ["idea","new","next"]
# dicta = {"idea": "meh", "new":"level","next":"shit"}


def read_file(file):
    with open(file,"r") as csv_file:
        reader = csv.DictReader(csv_file)
        data_from_file = [dict(story) for story in reader]

    return data_from_file


def write_file(file, data_list, fieldnames):
    with open(file, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(data_list)


def append_file(file, data_list, fieldnames):
    with open(file, "a") as csv_file:
        writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
        writer.writerow(data_list)


"""
new = read_file("sample_data/question.csv")
print(new)

for row in new:
    for key,value in row.items():
        print(f'{key}:{value}')
"""
"""



Common functions to read/write/append CSV files without feature specific knowledge.
The layer that have access to any kind of long term data storage. In this case, we use CSV files, 
but later on we'll change this to SQL database. So in the future, we only need to change in this layer.
"""