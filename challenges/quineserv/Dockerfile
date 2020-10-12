FROM python:3.7-alpine

ENV chdir /

COPY src/quineserv.py ${chdir}

WORKDIR ${chdir}

RUN apk add socat
RUN ln -s lib lib64
RUN ln -s ld-musl-x86_64.so.1 lib/ld-linux-x86-64.so.2

ENTRYPOINT ["socat", "-dd", "TCP4-LISTEN:5000,fork,reuseaddr", "EXEC:./quineserv.py,pty,rawer,stderr"]
#ENTRYPOINT ["/bin/sh"]

EXPOSE 5000
