FROM alpine:latest

ENV chdir /

COPY f71 ${chdir}

WORKDIR ${chdir}

RUN apk add socat
RUN ln -s lib lib64
RUN ln -s ld-musl-x86_64.so.1 lib/ld-linux-x86-64.so.2

ENTRYPOINT ["socat", "-dd", "TCP4-LISTEN:3954,fork,reuseaddr", "EXEC:'./f71 22 30',pty,stderr"]

EXPOSE 3954
