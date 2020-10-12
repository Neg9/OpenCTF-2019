# Easy 1

*Code by Javantea*  
Original idea July 22, 2017  
Updated to be solvable Mar 9-15, 2019

Score: 100

Description: Heap overflow one byte.

Category: pwnable

Build: `cd src; make easy1; mv -i easy1 ..`

## Notes

Exploitable and tested.  
The Makefile builds musl, arm, and win32 binaries by default for a reason, but we don't need the musl, arm, or win32 bins.
