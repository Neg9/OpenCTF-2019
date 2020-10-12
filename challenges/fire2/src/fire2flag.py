#!/usr/bin/env python3
"""
fire2flag.py
by Javantea
Jan 20, 2019

If you modify fire2.asm almost at all, you'll need to regenerate the flag.
Run nasm:
nasm fire2.asm
Run this script:
python3 fire2flag.py
Put the result instead of the values after msg db
This is very easy to automate, but I didn't want to do it.
"""

flag = b'flag{http://fabiensanglard.net/doom_fire_psx/ 0a4f0d9a1ab1f8c86b981f}\r\n\xff\x00'
fire = open('fire2','rb').read()[:len(flag)]
print(', '.join([str(x ^ y) for x,y in zip(flag, fire)]))
