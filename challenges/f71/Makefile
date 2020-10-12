# Makefile for f71

# -D_FORTIFY_SOURCE=0 is just for alpine. Dunno why.
CFLAGS = -O2 -ggdb -Wall -D_FORTIFY_SOURCE=0
LDFLAGS = -fPIC -fpie -fPIE

all: f71

f71: f71.o
engi: engi.o

clean:
	rm -f f71.o f71 engi.o engi
