# Makefile

# x86_64 because we're running on someone else's box.
CFLAGS = -O2 -ggdb -Wall -march=x86-64 -D_FORTIFY_SOURCE=0 -fno-stack-protector
ARM_CFLAGS = -O2 -ggdb -Wall -march=armv5t

LINUX_TARGETS = easy1 easy1.musl #easy2 easy3 easy4 
WIN32_TARGETS = easy1.exe #easy2.exe easy3.exe easy4.exe
ARM_TARGETS = easy1.arm #easy2.arm easy3.arm easy4.arm
TARGETS = $(LINUX_TARGETS) $(WIN32_TARGETS) $(ARM_TARGETS)

all: $(TARGETS)

# Unnecessary, but possible
%.musl: %.c
	x86_64-pc-linux-musl-gcc -o $@ $< $(CFLAGS) $(LDFLAGS)

%.exe: %.c
	i686-pc-mingw32-gcc -o $@ $< $(CFLAGS) $(LDFLAGS)

%.arm: %.c
	arm-unknown-linux-gnueabi-gcc -o $@ $< $(ARM_CFLAGS) $(LDFLAGS)

clean:
	rm -f $(TARGETS)
