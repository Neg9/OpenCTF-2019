#!/bin/sh
PASSWORD=$(python -c 'import string; import random; print("".join(([string.ascii_letters[random.randint(0,len(string.ascii_letters)-1)] for i in range(8)])))')
export PASSWORD
/home/$USER/minishell
