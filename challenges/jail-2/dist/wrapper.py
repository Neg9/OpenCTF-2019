#!/usr/bin/python3

import os
import sys
import subprocess
from functools import partial

flag = 'REDACTED'
max_length = 7

user_input = ''
while True:
    chunk = sys.stdin.read(256)
    if not chunk:
        break
    user_input += chunk

    if len(user_input) > max_length:
        print("Length: {}".format(len(user_input)))
        print("Too long!")
        sys.exit(3)

prohibited_funcs = ['system', 'exec', 'fork', 'print']

for prohibited_func in prohibited_funcs:
    if prohibited_func in user_input:
        print("No {}!".format(prohibited_func))
        sys.exit(1)

if '`' in user_input:
    print("No backticks!")
    sys.exit(2)

print("Length: {}".format(len(user_input)))

env = os.environ
env['flag'] = flag

p = subprocess.run(['perl', '-Mstrict', '-e', user_input], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
sys.stdout.buffer.write(p.stdout)
#if p.returncode:
#    sys.stdout.write('Process exited: {}\n'.format(p.returncode))
sys.stdout.flush()
