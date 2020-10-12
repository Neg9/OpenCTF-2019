# Super Eficient Key Store

*by ColdwaterQ*  

## Score
100

## Description
Check out this super cool Key store I made, it uses UDP to be super eficient and remove all that pesky tcp overhead. Mine is running on challenges.openctf.cat but I blocked the port so you will have to run your own. Feel free to remove that bit about "flag" some guy asked me to add it for his special project.


## Category
misc


## To run
This uses UDP so you need to start the docker file exposing those ports.

Note that the distributed source and server source differ. This was to prevent people from causing DoS scenarios, and allow it to be solveable without manually needing to setup connections. But it was tested considerably to try try and ensure that when used the server would act exactly like the client after setting it up.