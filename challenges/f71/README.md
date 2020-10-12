# F71

*by Javantea*  
Mar 21, 2019 and May 4, 2019

Score: 100

Description:
A graph game based on FTL but instead of there being fights at every jump, there is a party with aliens. You have to visit as many nodes as possible to win, 113 beers worth in fact. 

Category: misc

Solution is in solve.py

The solution could also be done very easily with the binary, which is why we aren't giving the users the binary. The number of nodes and connections can be tuned with the first and second parameter of the executable. 22 30 is enough for 134 beers if you run locally overnight. It's significantly faster remotely.

Remote:
```
real    0m0.462s
user    0m0.340s
sys     0m0.027s
```

Local:
```
real    0m18.725s
user    0m0.466s
sys     0m0.044s
```

```bash
sudo docker build --tag=f71 .
sudo docker run -p 3954:3954 f71
```
