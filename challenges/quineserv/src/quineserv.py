#!/usr/bin/env python3
"""
Quine server
by Javantea
May 4, 2019

Code execution as a service.
"""
from sys import modules, hexversion
modules.clear()
del modules

flag1 = 'flag{If only one of us could find the time. adeb4289b6a555}'
flag2 = "flag{A Sweet Sickeness, comes over me, I'm looking for something I want. lsUHNel2gLs}"

def sane_input(prompt='# '):
    """
    input(prompt) if Python didn't make python2 input(prompt).
    """
    if hexversion >= 0x3000000:
        return input(prompt)
    #end if
    return raw_input(prompt)
#end def sane_input(prompt)

inp = sane_input()
inp = inp[:1900]
#Dick move: you also have to only use the characters that my solution did.
inp = inp.encode('utf-8').translate(bytes(range(256)), b'')
if inp == b'':
    print("nothing is apparently a quine, but we don't want this to be that easy.")
    inp = b'===='
    exit(1)
#end if
v = ''
def mixprint(*args):
    """
    A print that doesn't do very interesting things. It's kinda similar to print.
    """
    global v
    r = ' '.join(['{{{0}}}'.format(i) for i in range(len(args))])
    v += r.format(*args)
#end def mixprint(*args)

exec(inp, {'__builtins__': {'print':mixprint, 'repr':repr, 'flag':''}}, {})

if v == inp.decode('utf-8'):
    print("You win level 1. {0}".format(flag1))
    v = ''
    exec(inp, {'__builtins__': {'print':mixprint, 'repr':repr, 'flag':flag2}}, {})
    print(v)
else:
    print("Quines win. You lose.")
    #print(repr(v))
    #print(repr(inp))
#end if

