FROM ubuntu:18.04

RUN apt-get update && apt-get install -y socat

RUN useradd -ms /bin/bash ctf

ADD ./src/rusty /home/ctf/rusty
ADD ./src/flag /home/ctf/flag
RUN chmod +x /home/ctf/rusty

USER ctf
WORKDIR /home/ctf

ENTRYPOINT ["socat", "-dd", "TCP4-LISTEN:5000,fork,reuseaddr", "EXEC:/home/ctf/rusty,pty,rawer,stderr"]
EXPOSE 5000
