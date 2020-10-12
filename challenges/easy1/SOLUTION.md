# Easy 1 Solution
*by Javantea*  
Jun 3, 2019

This flag is retrieved by overwriting one byte on the heap. It is made much more difficult by not providing the binary. The way to find the byte and the value you're supposed to give it is by looking at the responses.

```
ssh -L3001:challenges:9007 javantea@ctf.neg9.net
python3 easy1_solution.py
...
b'\n10240 1\nf149{heap_overflow_i5_an_art_not_a_sci3nce. Did you?}\n'

```
