#!/usr/bin/env python3
"""
Solution to AAAS
by Javantea
May 18, 2019
Oh dear how embarrassingly parallel this problem is.

python3 solve.py 2 &
python3 solve.py 3 &
python3 solve.py 4 &
python3 solve.py 5 &
python3 solve.py ein &
python3 solve.py sechs &
python3 solve.py elf &
python3 solve.py zwolf &
python3 solve.py gally &
wait

2 3 4 5 will end up going through their own if and then through the if at the bottom. This should solve in a matter of hours.

Maybe we should give them this script if it doesn't solve within the amount of time available in the contest, ~48 hours.

It took somewhere less than 203m
jvoss     3595 85.1  0.0  20548 11148 pts/10   R    18:40 203:35 /usr/lib/python-exec/python3.6/python3 solve.py ein
Use ein463157106@altsci.com
Quite a few more hours later:
Use 51879335342@altsci.com
Use zwolf2254083500@altsci.com
Use elf2383320740@altsci.com
Use 52452834664@altsci.com

"""
import random
import sys

def check(value):
    random.seed(value)
    a = random.randint(0, 0xffffffff)
    b = random.randint(0, 0xffffffff)
    return b == 987654321

# 1 failed.
if '1' in sys.argv:
    for i in range(0xffffff):
        email = 'john{0}@gmail.com'.format(i)
        if check(email.encode('utf-8')):
            print('Use', email)

if '2' in sys.argv:
    for i in range(0xffffff):
        email = 'dmitry{0}@altsci.com'.format(i)
        if check(email.encode('utf-8')):
            print('Use', email)

if '3' in sys.argv:
    for i in range(0xffffff):
        email = 'suzy{0}@altsci.com'.format(i)
        if check(email.encode('utf-8')):
            print('Use', email)

if '4' in sys.argv:
    for i in range(0xffffff):
        email = 'eric{0}@altsci.com'.format(i)
        if check(email.encode('utf-8')):
            print('Use', email)

if '5' in sys.argv:
    for i in range(0xffffff):
        email = 'david{0}@altsci.com'.format(i)
        if check(email.encode('utf-8')):
            print('Use', email)

if len(sys.argv) > 1:
    name = sys.argv[1]
    for i in range(0xffffffff):
        email = '{0}{1}@altsci.com'.format(name, i)
        if check(email.encode('utf-8')):
            print('Use', email)
else:
    # We have no names man, no names. We are nameless.
    for i in range(0xffffffff):
        email = '{0}@altsci.com'.format(i)
        if check(email.encode('utf-8')):
            print('Use', email)
