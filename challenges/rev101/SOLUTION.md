This binary takes an input, transforms it with rot13, and compares to a global
variable which has the rot13 of the flag.

There are two possible solutions.
One could use static analysis and a symbolic execution engine to get the key.
Or... you can just run `strings` on the binary, find the key string, and rot13
that for the flag.
