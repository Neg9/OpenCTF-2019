; basic rop
; author: drtychai
;
;  nasm -f elf64 challenge.asm && ld challenge.o && mv a.out challenge
;

              global    _start

              section   .text

_start:       call setid
              sub rsp, 0x24
              mov rdi, ask
              mov esi, 0x9
              call write
              lea rdi, [rsp-0x18]
              mov esi, 0x5a
              call read
              mov rdi, nom
              mov rsi, 0x10
              call write
              call exit

write:        mov rdx, rsi
              mov rsi, rdi
              mov eax, 0x1
              mov edi, 0x1
              call do_syscall
              ret

read:         mov rdx, rsi
              mov rsi, rdi
              mov eax, 0x0
              mov edi, 0x0
              call do_syscall
              ret

exit:         mov eax, 0x3c
              mov edi, 0x0
              call do_syscall

setid:        mov rdx, rsi
              mov rsi, rdi
              mov eax, 0x69
              mov rdi, 0x0
              call do_syscall
              ret

do_syscall:   syscall
              ret

set_rax:      pop rax
              ret

set_rdi:      pop rdi
              ret

set_rsi:      pop rsi
              ret

set_rdx:      pop rdx
              ret

ask:          db "FEED ME: "
              ret

nom:          db "NOM NOM NOM...", 0xa
              ret

binsh:        db "/bin/sh"
