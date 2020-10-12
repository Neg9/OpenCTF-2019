# Solution to Aliens 1

*by Javantea*  
*July 20, 2019*

The code is in base 3 intentionally obfuscated to ensure that a simple threshold won't be sufficient. One line is a numeral one, two lines is a numeral two, three lines is a numeral 3. This creates the orthogonal basis for an arithmetic system which can be translated into any other. 

https://www.altsci.com/concepts/base-n-math-without-zero

Take aliens1a.jpg, OCR the data. You will get:

|| ||| || ||| || || ||| | | || | || ||| ||| || | || || ||| ||| | | || ||| || || | || | ||| ||| | || | || | || || ||| | | ||| | ||| ||| ||| | ||| || ||| | | ||| || || | | || ||| | | | ||| || ||| || || | || | ||| || ||| | || || ||| || ||| | | ||| ||| || | ||| | || | || | || || || ||| ||| ||| | | | | | || || ||| | || || | | | || | ||| | ||| | ||| || | | | || || || | || | | ||| | | | ||| | | || | || | || || || | ||| || ||| ||| || | ||| || || | | | || ||| || | || || ||| | || | || | | || | ||| ||| || ||| ||| ||| | || ||| ||| || || || | | ||| | || || ||| | | | | ||| || | | ||| | || || ||| || || | | ||| || | | ||| || || || || || || ||| | || ||| ||| ||| ||| || || || | | || | ||| | || || ||| ||| | ||| | | || | ||| | | | || ||| || || ||| | ||| || | | || | | || || ||| ||| ||| ||| | ||| ||| | ||| ||| | | | | | | || ||| | ||| || ||| || ||| | ||| || | ||| | ||| ||| || || ||| | ||| ||| || || ||| | | | ||| | || || ||| || | || | || | ||| ||| ||| | || ||| | | | ||| || || || | || | ||| | || ||| || || ||| ||| | || | | || || | ||| | ||| ||| ||| | | | | || ||| ||| | | || || || | || ||| ||| | ||| ||| ||| || | | | | ||| | || ||| ||| || | || || | ||| | || | | ||| || | || | | | ||| ||| | ||| ||| || || || | | | || ||| || || | | || || | | || || ||| || || ||| | || || | ||| | | || || ||| ||| || | || | | | ||| | || ||| | || | ||| ||| | | | ||| | | ||| | ||| | | || | ||| | | || | || ||| | ||| || | ||| ||| || || || | ||| ||| || || ||| || ||| || ||| || || || ||| ||| || ||| ||| ||| || ||| || | | || | | ||| || || ||| || ||| | || ||| || || | ||| | | ||| ||| ||| ||| ||| | | || || || || || | | || | | ||| | || ||| || | | ||| ||| | ||| || || | ||| | | ||| || | || ||| ||| | || ||| || ||| ||| || || || ||| | | || | | || ||| || ||| || ||| || || | ||| ||| || || | ||| ||| || | | ||| | ||| || ||| ||| | || | || | | | ||| | | | | | | ||| ||| ||| ||| ||| | || ||| ||| ||| ||| || | ||| | | ||| || | | ||| ||| ||| ||| ||| || | | || || | || | ||| || ||| || | | || | | ||| ||| ||| | | | || | || || | | || ||| ||| ||| | | |||

The number of pipes is the data. Space is a delimiter. That converts directly to numbers:

2 3 2 3 2 2 ...

You have a problem that this won't directly convert to our zero-based math, so we subtract 1 from each to get numbers in the set {0, 1, 2}. This can then be multiplied into one number which becomes our value. I wish we didn't have to subtract, but I'm limited in the amount I can type.

Add and multiply. flag = sum([x*i**(l-v) for i, x in enumerate(data)])

See solve.py for an actual solution minus the OCR.
