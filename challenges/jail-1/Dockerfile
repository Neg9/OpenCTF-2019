FROM alpine:latest

WORKDIR /
RUN apk add socat python3 perl

COPY src/wrapper.py /
ENTRYPOINT ["socat", "-dd", "TCP4-LISTEN:5000,fork,reuseaddr", "EXEC:'./wrapper.py'"]

EXPOSE 5000
