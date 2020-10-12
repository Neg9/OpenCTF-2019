#!/usr/bin/env python3
"""
bin2asm.py
by Javantea
May 11, 2019
"""
import collections
import binascii
from sm5asm import LAX, OUT, TR, CALL, TL, ADX, SBX, RTN, HALT

flag = b'f149{Reversing the Nintendo 64 CIC - REcon 2015}'

naive_program = b''
for c in flag:
    # Naive method
    naive_program += LAX(c >> 4) + OUT() + LAX(c & 0xf) + OUT()

print(naive_program)
#b'\x16u\x16u\x13u\x11u\x13u\x14u\x13u\x19u\x17u\x1bu\x15u\x12u\x16u\x15u\x17u\x16u\x16u\x15u\x17u\x12u\x17u\x13u\x16u\x19u\x16u\x1eu\x16u\x17u\x12u\x10u\x17u\x14u\x16u\x18u\x16u\x15u\x12u\x10u\x14u\x1eu\x16u\x19u\x16u\x1eu\x17u\x14u\x16u\x15u\x16u\x1eu\x16u\x14u\x16u\x1fu\x12u\x10u\x13u\x16u\x13u\x14u\x12u\x10u\x14u\x13u\x14u\x19u\x14u\x13u\x12u\x10u\x12u\x1du\x12u\x10u\x15u\x12u\x14u\x15u\x16u\x13u\x16u\x1fu\x16u\x1eu\x12u\x10u\x13u\x12u\x13u\x10u\x13u\x11u\x13u\x15u\x17u\x1du'
len(naive_program)
#192
v = zlib.compress(naive_program)
#b'x\x9c-NQ\x16\x80 \x0c\xbaB\xb9i\xf9z\xd6)\xb9\x7f\x80\xfb@\xd8\x06s\x03\x03\x81\x93Hb\xe2\xc2\x83\x8e\xc6n\xa7\x1e\xc5\x8d\x08\xeaI\xbc\x84:\x07\xdf\xa4\xbe\xedQ\x9d\x9em\xcf\x9e\xf5\xf2K\x7f\xf6\x84\xff\xcb\xf2KM\xb3\xea\x86e\xd6\xb6t6\x9c\xd3\x8e\x9dm\xc4Q\xf7\xea\xae\x85\x1f\x8253\xd7'
len(v)
#93

# Trying to reduce the size a bit.
program = b''
prev_nibble = None
for c in flag:
    # Simple redundany removed method
    if prev_nibble != None and prev_nibble == (c >> 4):
        pass
    else:
        program += LAX(c >> 4)
    #end if
    prev_nibble = c >> 4
    program += OUT()
    if prev_nibble == (c & 0xf):
        pass
    else:
        program += LAX(c & 0xf)
    #end if
    program += OUT()
#loop

print(program)
#b'\x16uu\x13u\x11uu\x14uu\x19u\x17u\x1bu\x15u\x12u\x16u\x15u\x17u\x16u\x16u\x15u\x17u\x12uu\x13u\x16u\x19uu\x1euu\x17u\x12u\x10u\x17u\x14u\x16u\x18uu\x15u\x12u\x10u\x14u\x1eu\x16u\x19uu\x1eu\x17u\x14u\x16u\x15uu\x1euu\x14uu\x1fu\x12u\x10u\x13u\x16uu\x14u\x12u\x10u\x14u\x13uu\x19uu\x13u\x12u\x10uu\x1duu\x10u\x15u\x12u\x14u\x15u\x16u\x13uu\x1fuu\x1eu\x12u\x10u\x13u\x12uu\x10uu\x11uu\x15u\x17u\x1du'

len(program)
#171

# Significantly shorter than 192, the natural program with no ifs.

v2 = zlib.compress(program)
#b'x\x9c5\x8e\xdb\r\xc0 \x0c\x03W\xa0<[U\xc0\x94\xb7\x7fm\xa2\xfe\x1c2\xb6\x93t(\\P\xe1a\xf0\xd2\xc8tq\x88\xf1fG\xbal\x16G&\xb1\xea\xe7\xe6\xa4\x93\xc4\xfa\x03\xe1\xb4\x93\xd5\xcc}|\xd7\xa5"Z\xbcI\xb4b"zH\x15\xbb\xbd\xedj\x94\xb2M\x1f\xe7+&\x1f\xb5\xc92&'
len(v2)
#90

# So we're down to minimial at 90 bytes. Let's see if we can find functions.

set(program)
#{16, 17, 18, 19, 20, 117, 22, 23, 21, 25, 24, 27, 29, 30, 31}

# We've really reduced the program to a tiny set.

c = collections.Counter()
c.update([program[i:i+4] for i in range(len(program)-4)])
c.most_common(6)
[(b'u\x12u\x10', 6), (b'\x12u\x10u', 6), (b'uu\x1eu', 4), (b'uu\x13u', 3), (b'uu\x14u', 3), (b'u\x15u\x12', 3)]

# using a window I was able to find a few functions I can make to replace 4 bytes with 2. So...

func = b'\x12u\x10u' + RTN()
func_addr = 0

program2 = func + (program.replace(b'\x12u\x10u', CALL(func_addr)))

len(program2)
#164

# Righteous coding dude.

p2c = zlib.compress(program2)
#b"x\x9c-\x8e\xc9\x11\x800\x0c\x03S\x02\xe4p`\x98@\x95\xfb\xa4\xe7\x94\x80\x04|d\xc7+[\xc9,\xdc\x01\x85\x15*\xect\x0e\x1a\x99\x90v\xe9W\xb3-!\xcc\x89\x9e3u\xb9\x83\r\xd1\x99\xaa\xa6?\xfc\xe6\xed\xf5\xe9\xde%\xeaE\xf5\xb6\x15'Hgb\xa0h\x07Ui\x98\\^\xb2=\x1b\xf9CN\x1e<'\xa63\x07"
len(p2c)
#97
# It's bigger than either because it has more possible values probably.

# Will it run?
open('program2.bin','wb').write(program2)

# No because I put the function at the beginning.

program2 = TR(len(func)) + func + (program.replace(b'\x12u\x10u', CALL(func_addr))) + HALT()

# The previous one tries to return as second instruction.

program2 = TR(len(func)+1) + func + (program.replace(b'\x12u\x10u', CALL(func_addr))) + HALT()

# It ran and printed stuff, but not what we wanted. Nice try though.

binascii.unhexlify('663114497b526576657223699ee7663114497b526576657223699ee7663114497b526576657223699ee7663114497b526576657223699ee7663114497b526576657223699ee7')
#b'f1\x14I{Rever#i\x9e\xe7f1\x14I{Rever#i\x9e\xe7f1\x14I{Rever#i\x9e\xe7f1\x14I{Rever#i\x9e\xe7f1\x14I{Rever#i\x9e\xe7'
