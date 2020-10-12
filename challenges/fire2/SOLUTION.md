# Fire 2 Solution
*by Javantea*  
Jan 20, 2019

The point of this challenge is to illustrate the boot sector program. If you can figure out qemu and gdb, you're golden. If you can reverse 8086 (yes, it's 16-bit 8086), you might or might not catch the xor of the program and itself. If you can modify a program to add a debug or a sleep, you'll get a wrong answer.

```bash
qemu-system-i386 ../../8086/fire2

ctrl-alt-2
gdbserver

gdb
target remote localhost:1234
b *0x7c13
c
```

Use qemu gui to select Machine / Reset

```
Breakpoint 1, 0x00007c13 in ?? ()
(gdb) x/s 0x7c82
0x7c82: "f149{http://fabiensanglard.net/doom_fire_psx/ 0a4f0d9a1ab1f8c86b981f}\r\n\377"
```

An easier solution is simply:

```
fire = open('../../8086/fire2','rb').read()
bytes([(x ^ y) for x,y in zip(fire[:73], fire[0x88:0x88+73])])
```

A more general solution can be found in solve.py:

```python
fire = open('dist/fire2','rb').read()
for offset in range(len(fire)):
	flag = bytes([(x ^ y) for x,y in zip(fire[:73], fire[offset:offset+73])])
	if flag.startswith(b'f149{'):
		print(flag, hex(offset))
	#end if
#next offset
```

The flag is `f149{http://fabiensanglard.net/doom_fire_psx/ 0a4f0d9a1ab1f8c86b981f}`
