name: MegaHash301
category: crypto
author: AnthraX101
final score: 99 points


## Overview

This challenge asks you to attack a chained cipher that is a sequence of a large number of cryptographic hash algorithms. 

Connect to the web server. This challenge asks you to find a second preimage that matches a given hash value with a large (~100,000) iteration count this time.

## Build

Use Python 3.7 and either:
    pip install web.py==0.40-dev1
Or for Ubuntu/Docker:
    apt-get install -y python3-webpy 

## Run

Use RealWebServer.py, -not- WebServer.py. RealWebServer hardcodes the CSPRNG so different instances don't have different target hashes, as well as having a fairly "worst case" target. Because the search space is so small, not all outputs are equally likely, this output makes the user search more of the input space to find it...

RealWebServer additionally uses a substantially more efficient hashing algorithm normally used to solve 302. While the solution to 301 would work to run this server, it would induce several minutes of calculation load at startup. Don't peak at any of the EfficientMegaHashes before solving both 301 and 302 if avoiding spoilers.

Use python 3.7 only. 
