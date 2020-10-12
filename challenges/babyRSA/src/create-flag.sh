#!/bin/bash
openssl rsautl -encrypt -inkey public.key -pubin -in flag.txt -out flag.enc
