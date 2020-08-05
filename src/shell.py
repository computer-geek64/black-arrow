#!/usr/bin/python3
# shell.py

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from time import sleep
from config import REFRESH_DELAY


with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stdout.lock'), 'w') as lock:
    lock.truncate()

while True:
    command = input('>> ')
    if command == 'exit':
        break
    elif command == 'init_bash':
        command = ''
    elif command == 'init_powershell':
        command = ''
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'command.lock'), 'w') as lock:
        lock.write(command)

    for i in range(REFRESH_DELAY):
        sleep(1)
        if os.stat(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stdout.lock')).st_size > 0:
            break
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stdout.lock'), 'r+') as lock:
        print(lock.read())
        lock.seek(0)
        lock.truncate()
