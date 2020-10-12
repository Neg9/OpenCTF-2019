# GDB2 Solution

*by Javantea*  
Jan 19, 2019

The point of this exercise is to teach people what the gdb protocol is actually doing. It doesn't take a lot of work. You can use gdb and gdbserver like so:

```
gdbserver localhost:4009 /bin/ls
gdb
target remote tcp::4009
```

This allows you to write code to search for things. Things like flags and such. In this challenge, the flag is hidden a little bit too well. I'd like to fix that, but I decided to stop working on it as soon as it started working. Feel free to improve it.


Step 1: Run gdb and search for memory.

```
gdb
GNU gdb (Gentoo 8.2.1 p1) 8.2.1
Copyright (C) 2018 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-pc-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://bugs.gentoo.org/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word".
(gdb) target remote tcp::4009
Remote debugging using tcp::4009
Reading /bin/ls from remote target...
warning: File transfers from remote targets can be slow. Use "set sysroot" to access files locally instead.
Reading /bin/ls from remote target...
Reading symbols from target:/bin/ls...Reading /bin/ls.debug from remote target...
Reading /bin/.debug/ls.debug from remote target...
Reading symbols from /home/debug/bin//ls.debug...(no debugging symbols found)...done.
(no debugging symbols found)...done.
warning: unable to open /proc file '/proc/22107/task/22107/maps'
warning: Unable to find dynamic linker breakpoint function.
GDB will be unable to debug shared library initializers
and track explicitly loaded dynamic code.
0x00007ffff7fd6210 in ?? ()
(gdb) x/10s $rip
0x7ffff7fd6210: "\006"
0x7ffff7fd6212: "\006"
0x7ffff7fd6214: "\006"
0x7ffff7fd6216: "\006"
0x7ffff7fd6218: "\006"
0x7ffff7fd621a: "\006"
0x7ffff7fd621c: "\006"
0x7ffff7fd621e: "\006"
0x7ffff7fd6220: "\006"
0x7ffff7fd6222: "\006"
(gdb) x/10s $rsp
0x7fffffffd5e0: "\006"
0x7fffffffd5e2: "\006"
0x7fffffffd5e4: "\006"
0x7fffffffd5e6: "\006"
0x7fffffffd5e8: "\006"
0x7fffffffd5ea: "\006"
0x7fffffffd5ec: "\006"
0x7fffffffd5ee: "\006"
0x7fffffffd5f0: "\006"
0x7fffffffd5f2: Ignoring packet error, continuing...
Reply contains invalid hex digit 123
```

Step 2: Once you notice that address 0x7fffffffd5f2 results in a packet error, check the tcpdump or use the following to repro:

```
(echo -n '$m7fffffffd5f2,8#03'; sleep 1) | nc localhost 4009
+$f149{everything is everything e759d9c47a13e4974756e911cafc19f9755c37141ee6a3a76ac0df6ac358f561a0b623483cf6d1006f994d806e6957bd72a9f4c6ca9cce1d1c6530fe25c1fe05}

The flag is f149{everything is everything e759d9c47a13e4974756e911cafc19f9755c37141ee6a3a76ac0df6ac358f561a0b623483cf6d1006f994d806e6957bd72a9f4c6ca9cce1d1c6530fe25c1fe05}

```
