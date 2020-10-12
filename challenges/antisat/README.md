# antisat.exe
*by Javantea*

Original Idea: May 24, 2016  

Score:
97

Solution: solve.py

Description: A simple sat solve problem. Or you could just use python.

Category: Reversing, Crypto

Build: If you actually want to build this, you need a working x86_64-w64-mingw32-gcc which can be gotten with Gentoo crossdev.

Requirements:
* Windows 64 (not)

How to run:
```
wine antisat.exe 1
```

How to exit:
Ctrl-C will exit

Challenge Text:

Our cluster just locked up. Could you see why our sat solver isn't tearing through this? It's a standard Windows 64 binary.

Notes:
It's not stripped and has debug turned on kinda for a reason. We could strip if we wanted to make the reverse engineering difficult.
