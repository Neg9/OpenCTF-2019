FROM alpine:latest

ENV chdir /

COPY dist/easy2 ${chdir}
COPY src/flag ${chdir}

WORKDIR ${chdir}

RUN apk add socat
RUN ln -s lib lib64
RUN ln -s ld-musl-x86_64.so.1 lib/ld-linux-x86-64.so.2

ENTRYPOINT ["socat", "-dd", "TCP4-LISTEN:3001,fork,reuseaddr", "EXEC:./easy2,pty,rawer,stderr"]

EXPOSE 3001
