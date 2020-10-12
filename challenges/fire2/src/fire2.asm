; https://wiki.osdev.org/Babystep2
; red.asm
; http://fleder44.net/312/notes/18Graphics/index.html

; red
;; by Javantea
;;; Sept 22, 2017 - Jan 20, 2019
;;;;; For Neg9's CTF or OpenCTF

; red writes the decrypted flag to the screen using int 10 ah=0xe. Then it clears the screen red before the user can read it.
; Added a sleep so that you can see it. But really... that sleep.. zzzzzz

; flag's origin is sha512sum ../../8086/fire.asm
; 0a4f0d9a1ab1f8c86b981f92bfa6858a8568d501085e3acdfdee21b593236fe508bf1d04142f7ca59aab2f19e0838258ff4d363697cb5b20ed3729129a6cd4b0  ../../8086/fire.asm

; FIXME: there's an off by one somewhere so that it starts 

%define KEY 0x42

   mov ax, 0x07c0
   mov ds, ax

   jmp main
   
print_si:lodsb ; load byte ds:[si] into al, incrementing si
   ;inc ax
   or al, al ; zero=end or str
   jz end   ; get out
   mov ah, 0x0E
   int 0x10
   jmp print_si
end:
   ret

main:

print_msg:
   mov si, bang

; we want to run decrypt twice, so... the cmp je does that.

top_decrypt:
   ; this is the point of this lesson: self-referential decryption.
   ; if you change the algorithm at all, you wreck it. have fun you fucking hackers!
   ; flag = b'f149{http://fabiensanglard.net/doom_fire_psx/ 0a4f0d9a1ab1f8c86b981f}\r\n\xff\x00'
   ; fire = open('../../8086/fire2','rb').read()[:len(flag)]
   ; bytes([(x ^ y) for x,y in zip(flag, fire)])
   ; b'\xde\xf13\xb7\xa3\x83x\xd8x\xfa[)\xd2o\xafy\x8e\x9b\xb0\xdf\xadg\xe6-\xf4T" \xe4\x8aUd\x12\x9b\x85\xbd\x99\x81ee\xb4\x99\x87\x93\xd2\x9a\xcf\x9e\xdc`0,Mc\xda\x94\xa1{\x12:\x88\xc3\xf5\xd988\x89fm'
   ; print(', '.join([str(x ^ y) for x,y in zip(flag, fire)]))
   ; 222, 241, 51, 183, 163, 131, 120, 216, 120, 250, 91, 41, 210, 111, 175, 121, 142, 155, 176, 223, 173, 103, 230, 45, 244, 84, 34, 32, 228, 138, 85, 100, 18, 155, 133, 189, 153, 129, 101, 101, 180, 153, 135, 147, 210, 154, 207, 158, 220, 96, 48, 44, 77, 99, 218, 148, 161, 123, 18, 58, 136, 195, 245, 217, 56, 56, 137, 102, 109
   ; to make this far more difficult we could use encryption, because encryption would make this annoying.
   mov cl, [si-msg]
   ;xor WORD [si], cx
   xor BYTE [si], cl
   dec si
   cmp si, msg
   jge top_decrypt
   
   call print_si
   
   ; print the message a second time in case they missed it! =D
   ; modifying this results in a failed decrypt.
   cmp BYTE [msg], 'f'
   je print_msg
   
to_remind_you_theres_life_after_school:
   call red
   ; we're done, stick a fork in us.
   ;jmp hang
   ; or not. loop
   ;jmp main
   jmp to_remind_you_theres_life_after_school
 
hang:
   hlt
   jmp hang

   ; sleep(ax)
sleep:
	; for(; ax != 0; ax--) {
	;    sleep2(0xffff);
	;}
	mov dx, 0xffff
	call sleep2
	dec ax
	je end_sleep
	jmp sleep
	end_sleep:
	ret

   ; sleep2(dx)
sleep2:
	;for(; dx != 0; dx--) {
	;}
	dec dx
	je end_sleep2
	jmp sleep2
	end_sleep2:
	ret

red:
	mov bx, 0x1;0xf000
top1:
	mov ax, 0x1000
	;call sleep
	dec bx
	je end_redsleeps
	jmp top1
end_redsleeps:

	; set video mode
	mov ah, 0x0
	; Text Mode: 0x3
	; Graphics: 0x4
	mov al, 0x84
	int 0x10
	
	; clear window to red
	;mov ah, 0x6
	;mov cx, 0x0000 ; upper left corner (0x0, 0x0)
	;mov dx, 0x184f ; lower right corner (0x4f cols, 0x18 rows) # 0x174e is minus one row and one col
	;mov bh, 0x4e ; 3 == cyan foreground, 4 = red background.
	;int 0x10
	
	; change the background to red
	mov ah, 0xb
	mov bx, 0x0014
	int 0x10

	; move cursor to middle
	mov ah, 0x2
	mov dx, 0x0720 ; (0x7 rows, 0x20 cols)
	mov bh, 0x0
	int 0x10
	; draw some text again.
	;mov si, msg
	;call print_si

	; draw the program itself.
	;pop si
	;push si
	;sub si, ($ - $$)
	xor si, si
	
	; set color palette
	mov ah, 0xb
	mov bh, 0x1
	mov bl, 0xb
	int 0x10
	
	; foreground color!
	mov bl, 1

top3:
	cmp si, 0x200
	ja done_printing
	;mov si, 0x7c0
	call print_si
	inc si
	mov ax, 0x100
	jmp top3
done_printing:
	;call sleep
	; You're not done printing! hahahaa
	xor si, si
	jmp top3
	; return to main
	ret
	
; encrypted flag, starts with f149{ and ends with } ff 00
msg db 222, 172, 102, 233, 163, 131, 120, 216, 120, 250, 91, 41, 210, 111, 175, 121, 142, 155, 176, 223, 191, 103, 230, 237, 10, 155, 30, 98, 43, 245, 209, 236, 111, 18, 158, 183, 135, 150, 242, 91, 215, 112, 21, 12, 201, 200, 39, 97, 223, 157, 196, 143, 196, 219, 206, 158, 138, 55, 102, 112, 23, 58, 221, 151, 250, 114, 69, 100, 150, 246, 201, 68, 1
;msg db 'f149{http://fabiensanglard.net/doom_fire_psx/ 0a4f0d9a1ab1f8c86b981f}', 13, 10, 255, 0
bang db '!', 13, 10, 255, 0
   
   times 509-($-$$) db 1
   db 0x0
   db 0x55
   db 0xAA

have_a_fun_time:
	mov si,msg
top2:
	stosb ; write al to msg[si]
	;or al, al
	inc ax
	
	;jz print_msg
	jmp top2
