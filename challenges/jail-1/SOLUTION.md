The challenge runs the user input as a perl script, filtering out some useful functions including print, and putting the flag in the environment. My solution, which doesn't need as many characters as you're limited to, is to exfil each character of the flag through the exit code.

