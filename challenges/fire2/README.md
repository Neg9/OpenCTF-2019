# Fire 2

Original Idea: 2017-09-22  
Written: 2017-09-22-2019-01-20

Score: 94

Description: 8086 hand-written assembly. Self-referential encryption. Easy to solve if you know what is going on.

Category: Reversing

Build:
* `nasm -o dist/fire2 src/fire2.asm`
* If you change the flag, you need to run `fire2flag.py` and then modify src/fire2.asm and then reassemble.

Solution: solve.py

Requirements:

How to run:
qemu-system-i386 fire2

How to exit:
Close Qemu

Challenge Text:

This is the second worst fire animation I've seen. It was hand coded? Artisinal you say? 210 bytes? 8086 assembly? Genius, mad genius.
