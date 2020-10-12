#FROM alpine:latest
FROM ubuntu:18.04

ENV USER mini

WORKDIR /home/$USER

# ubuntu 
RUN useradd $USER
RUN apt-get update
RUN apt-get dist-upgrade -y
RUN apt-get install -y socat libc6-i386 python

# alpine 
#RUN adduser -D $USER
#RUN apk add socat python

COPY dist/minishell /home/$USER/
COPY minishell.sh /usr/local/bin/minishell
COPY flag /home/$USER/flag

# make sure all files owned by root (but readable by user) 
# allow read and list files in the directory, but not create or delete files
RUN chown -R root:$USER /home/$USER
RUN find /home/$USER -type d -exec chmod 550 {} \;
RUN chmod 550 /home/$USER/minishell
RUN chmod 555 /usr/local/bin/minishell
RUN chmod 440 /home/$USER/flag

USER $USER

ENTRYPOINT ["socat", "-d", "-d", "TCP4-LISTEN:5000,fork,reuseaddr,forever", "EXEC:'/usr/local/bin/minishell',sighup,sigint,sigquit"]

EXPOSE 5000

