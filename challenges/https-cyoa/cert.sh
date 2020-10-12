#!/bin/sh

# Key and CSR
openssl req -new -keyout server2.pem -out server2.csr

# Sign CSR with Key (self-signed)
openssl x509 -signkey server2.pem -req -in server2.csr -out server2.crt -days 365

# decrypt key
openssl rsa -in server2.pem -out server2clear.pem

# Combine clear key and cert
cat server2clear.pem server2.crt >certkey.pem
