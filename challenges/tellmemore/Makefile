CC = gcc
CFLAGS = -W -Wall

all: dist/tellmemore

dist/tellmemore: src/tellmemore.c
	$(CC) $(CFLAGS) -o $@ $<
	strip -s $@

clean:
	rm dist/tellmemore
