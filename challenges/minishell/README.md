#minishell

type: pwnable
author: meta
final score: 100

## Description

Already know you that which you need. 

## Build

Build prerequisites on an Ubuntu 18.04 system

```
apt install gcc-multilib libc6-i386
```

Current binary for distribution was built and tested with clang

```
clang -m32 -fno-common -o dist/minishell src/minishell.c
```

Could be built with gcc (optional)
```
gcc -fno-stack-protector -m32 -no-pie -o mini minishell.c
```


## Run

The challenge needs an environment variable with the password set.

```
PASSWORD=ABCD1234 socat -d -d tcp4-l:5000,fork,reuseaddr exec:./mini
```

