#FROM alpine:latest
FROM ubuntu:18.04

ENV USER hash302

WORKDIR /home/$USER

# ubuntu 
RUN useradd $USER
RUN apt-get update
RUN apt-get dist-upgrade -y
RUN apt-get install -y python3 python3-webpy 

# alpine 
#RUN adduser -D $USER
#RUN apk add python3

COPY dist/MegaHash.py /home/$USER/
COPY dist/sha1.js /home/$USER/
COPY solution/RealWebServer.py /home/$USER/
COPY solution/EfficientMegaHashN.py /home/$USER/
COPY flag.txt /home/$USER/

# make sure all files owned by root (but readable by user) 
# allow read and list files in the directory, but not create or delete files
RUN chown -R root:$USER /home/$USER
RUN find /home/$USER -type d -exec chmod 550 {} \;
RUN chmod 440 /home/$USER/*

USER $USER

ENTRYPOINT ["/usr/bin/python3", "-u", "/home/hash302/RealWebServer.py"]

EXPOSE 8000

