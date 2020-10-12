# Makefile for m68hc11

#THISDIR=$HOME/m68hc11/
#
#mkdir build-m68hc11 && cd build-m68hc11
#../configure --target=m6811-elf --program-prefix=m6811-elf-
#make -j9
#make install DESTDIR=$THISDIR

AS=m6811-elf-as
CC=m6811-elf-gcc
LD=m6811-elf-ld

all: makemyday test1e104

test1e104: test1e104.o
	$(LD) -o $@ $<

%.o: %.S
	$(AS) -o $@ $< -ggdb

makemyday: makemyday.o
	m6811-elf-ld -o makemyday makemyday.o

