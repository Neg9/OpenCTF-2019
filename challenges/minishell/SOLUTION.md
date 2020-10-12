

# Minishell solution

The solution to minishell has been codified in solve.py, the human readable explanation is as follows.

minishell is a 32-bit Linux ELF executable with a NX stack, ASLR enabled, but no stack canaries. 
The shell implements a bash like shell that supports the following commands
   * cd
   * ls
   * pwd
   * cat
   * echo (useless) 
   * help (easter egg)
   * sudo (easter egg)

The user will be able to traverse the filesystem, discover the flag file, but when they try to cat it
they will told "Lol, nice try". The goal is to discover the exploit and cat the flag.

The binary reads a PASSWORD from an environment variable on start and compares a static string to
that password. If they hard coded password is the same as the environment variable, it bypasses the
check for the string "flag" in the filename of the cat command. However, there is no way to actually
set this variable, it's a static string in the binary on the stack.

The minishell binary has a 1-byte stack overflow in the input, as such, they can control the least
significant bit of the frame pointer (EBP) but nothing else. The intended solution is to use control
of the frame pointer to shift the stack such that the password environment variable is compared to
a string on the stack under the users control. This will make it possible to cat the flag file.

However, as an additional complexity, the password will not be brute forcible, nor is there any information
disclosure in the binary to discover it. However, because you can traverse the file system and cat 
arbitrary file contents, you'll be able to cat /proc/self/environ to discover the correct password.

Finally, because ASLR is enabled, the stack address will actually change every execution. This will require
a certain amount of guessing to get the right alignment, but there are only 256 possibilities and, 
in practice, the alignment will happen with about a dozen tries. 

The entire solution is in `solve.py`.


## To test solution against challenge server

1. ssh -L 9019:challenges:9019 ctf.neg9.net
2. python src/solve.py   
3. wait about 1 minute for flag



