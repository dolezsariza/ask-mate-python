from flask import Flask, request, redirect, render_template, url_for

import csv

def read_file(file):
    with open(file,"r") as csv_file:
        reader = csv.DictReader(csv_file)
        user_stories = [dict(story) for story in reader]

    return user_stories

# print(read_file("sample_data/question.csv"))
"""


Common functions to read/write/append CSV files without feature specific knowledge.
The layer that have access to any kind of long term data storage. In this case, we use CSV files, 
but later on we'll change this to SQL database. So in the future, we only need to change in this layer.
"""