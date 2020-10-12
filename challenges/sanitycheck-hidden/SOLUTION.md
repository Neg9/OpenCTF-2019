This is hidden within "sanity check" and can be exploited with rop.

Challenge is a static binary with all the fixin' built in. Solution is to construct a payload that uses included gadgets with `do_syscall()` to call `execve("/bin/bash",NULL,NULL)`.

