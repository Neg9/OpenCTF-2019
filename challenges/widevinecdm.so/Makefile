# Makefile for binary.wasm (sq.c)

CFLAGS=-ggdb -O2 -Wall -ansi

DOUBLE_CFLAGS=-DTEST $(CFLAGS)

all: binary.wasm double.so double double.wasm

binary.wasm: sq.c
	clang -cc1 -Ofast -emit-llvm-bc -triple=wasm32-unknown-unknown-wasm -std=c11 -fvisibility hidden sq.c 
	llvm-link -o wasm.bc sq.bc 
	opt -O3 wasm.bc -o wasm.bc
	llc -O3 -filetype=obj wasm.bc -o wasm.o
	wasm-ld --no-entry wasm.o -o binary.wasm --strip-all -allow-undefined-file wasm.syms --import-memory

double.so: double.c
	$(CC) -o $@ $^ $(CFLAGS) -shared -fPIC

double: double.c
	$(CC) -o $@ $^ $(DOUBLE_CFLAGS) -pie

%.bc: %.c
	clang -cc1 -Ofast -emit-llvm-bc -triple=wasm32-unknown-unknown-wasm -std=c11 -fvisibility hidden $^

# FIXME: this is way wrong. Do not do this!
%.wasm: %.bc
	opt -O3 $^ -o $^
	llc -O3 -filetype=obj $^ -o $^.o
	wasm-ld --no-entry $^.o -o $@ --strip-all -allow-undefined-file double.syms --import-memory

