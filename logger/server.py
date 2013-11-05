'''
Created on 4 nov. 2013

@author: Teunissen-S
'''
from flask import Flask


def create_flask():
    app = Flask(__name__)
    #app.add_url_rule('/getlog', 'get_log_file', get_log_file)
    return app


def get_log_file():
    pass

