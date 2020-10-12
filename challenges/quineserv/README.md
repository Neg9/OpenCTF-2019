# Quineserv

*by Javantea*  
Mar 21, 2019 and May 4, 2019

Score: 64

Description:
Electric Frankenstein wrote this service. I think it is going a little too far into Gödel Escher Bach if you ask me. But at least it tells you when you accidentally infect the laboratory with a virus.


Category: misc

Flag 1: Give me a quine to get the flag. Solution is quine2b_solve.py.

Flag 2 (see Return to Quineserv): Give me a quine that prints the flag. Solution is quinef2_solve.py.

```bash
sudo docker build --tag=quineserv .
sudo docker run -p 3002:3001 quineserv
```
