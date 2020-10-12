
# Solution

There are three discrete but sequential challenges on the ATTiny85 hw hacking challenge.

The following PDF shows the PIN diagram, note that pins 0-4 are labeled in blue.
https://cdn.sparkfun.com/assets/2/8/b/a/a/Tiny_QuickRef_v2_2.pdf


## Level 2

This one is harder. The serial terminal prompts for "flag:" every few seconds and the user
needs to enter the flag. Careful analysis will reveal a timing side channel attack in the 
string compare. This has been very carefully orchestrated to be solvable with the inherently 
slow connection of a serial terminal. The solution is to write a script to iterate through 
the alphabet and compare the timing side channel to iteratively brute force each character
of the 20 character flag (ascii lowercase). 

See `solve.py` script for complete implementation of side channel attack.

```
flag: 
flag: 
flag: 
flag: uareahwhackerxoruart  <---- Woot! That's the flag :)
Well done angelheaded hipster; the stary dynamo awaits.
Welcome to level 3!
```

