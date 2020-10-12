#!/bin/sh -e

executable="/parricide"
listen_port=5000
cookie=$(dd if=/dev/urandom bs=1 count=16 status=none | xxd -ps)

# -T: 10 Second timeout
# -d -d: debug to console
# -lp: Set prefix of socat env variables to a random cookie to hide that we're using socat in case someone got shell injection
socat -T 10 -d -d -lp "$cookie" "TCP-LISTEN:${listen_port},reuseaddr,fork" "SYSTEM:${executable}"
