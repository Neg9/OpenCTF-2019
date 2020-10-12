#!/bin/bash

for i in $(seq 0 9); do cp -i video720.png video720_0"$i".png ; done

for file in video_cover.mp4 flag2b.mp4; do echo "file '$file'"; done >flag2b1.txt
ffmpeg -f concat -i flag2b1.txt -c copy flag2b1.mp4

