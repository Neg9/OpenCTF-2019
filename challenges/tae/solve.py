#!/usr/bin/python3
import re
import sys
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 5000))

# get the key
msg = sock.recv(1024)
key = re.match(
    "If you can make me say ([0-9a-f]{40}) then I will tell you the flag.", msg.decode("utf-8")
).group(1)

for _ in range(2300):
    sock.send(f"{key} {msg.decode()}\n".encode())
    resp = sock.recv(1024).decode()
    if key in resp:
        while True:
            if "flag{" in resp:
                print(resp)
                sys.exit(0)
            else:
                resp = sock.recv(1024).decode()
