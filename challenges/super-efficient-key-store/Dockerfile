FROM alpine:latest

RUN apk add --no-cache musl-dev go

# Configure Go
ENV GOROOT /usr/lib/go
ENV GOPATH /go
ENV PATH /go/bin:$PATH

RUN mkdir -p ${GOPATH}/bin ${GOPATH}/src

COPY src/ /go/src/udp
RUN go install udp

WORKDIR /go/src/udp

ENTRYPOINT udp

EXPOSE 12000-13000/udp
