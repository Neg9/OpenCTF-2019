#!/usr/bin/env python3
"""
Blight1a
by Javantea
Feb 17, 2019

A script to make Blight 1 more difficult!
Take a string that is helpful to the user and embed it in the stream.
It corrupts the flag{ portion, but not enough to actually break the flag because Gaussian FSK.
"""
import random
a = open('blight1.bin','rb').read()
pos = random.randint(0, 15)
ax = b''
for i in b'are you still looking here?':
	ax += a[len(ax):pos] + bytes([i])
	pos += random.randint(0, 15)

ax += a[len(ax):len(a)]

open('blight1a.bin','wb').write(ax)                      

keystream = []
pos = 0

for i in b'are you still looking here?':
	x = ax.find(i, pos+1)
	keystream.append(x)
	pos = x

keystream = [9, 16, 19, 20, 30, 31, 44, 45, 54, 64, 74, 86, 87, 102, 111, 123, 134, 148, 156, 171, 182, 196, 209, 212, 222, 234, 247]
