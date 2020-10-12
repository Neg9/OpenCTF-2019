CC = gcc
CFLAGS = -W -Wall

all: dist/rev101

dist/rev101: src/rev101.c
	$(CC) $(CFLAGS) -o $@ $<
	strip -s $@

clean:
	rm dist/rev101
