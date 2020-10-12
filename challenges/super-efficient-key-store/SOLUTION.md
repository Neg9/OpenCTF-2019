1. Review the provided source code and run it locally if you want.
2. Observe that you can directly connect to the UDP ports after the user has entered the secret to hijack their session
3. Send a UDP packet containing "get flag" to each port between 12000 and 13000.
4. To test the solution you can run "nc -u 104.248.208.235 12021" and then type "get flag" and press Enter

port 12021 is hard coded to be the port with the flag.