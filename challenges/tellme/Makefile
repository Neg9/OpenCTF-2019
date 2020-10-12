CC = gcc
CFLAGS = -W -Wall

all: dist/tellme

dist/tellme: src/tellme.c
	$(CC) $(CFLAGS) -o $@ $<
	strip -s $@

clean:
	rm dist/tellme
