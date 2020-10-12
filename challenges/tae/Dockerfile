FROM alpine:latest

RUN apk update && apk add --no-cache --virtual=go_build \
    musl-dev \
    go

# Configure Go
ENV GOROOT /usr/lib/go
ENV GOPATH /go
ENV PATH /go/bin:$PATH

RUN mkdir -p ${GOPATH}/bin ${GOPATH}/src

COPY src/ /${GOPATH}/src/tae
COPY src/taetae.txt /taetae.txt
RUN go install tae
RUN rm -rf ${GOPATH}/src
RUN apk del go_build

WORKDIR /

ENTRYPOINT ["/go/bin/tae"]

EXPOSE 5000
