# Makefile for sm5 aka Game Copy Protection ROM

all: dump.bin

dump.bin: sm5_flag.o
	cp sm5_flag.o dump.bin

sm5_flag.o: sm5_flag.S
	python3 sm5asm.py -o sm5_flag.o sm5_flag.S

