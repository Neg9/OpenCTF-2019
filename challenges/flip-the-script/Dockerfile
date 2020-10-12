FROM alpine

RUN apk update

RUN apk add nodejs

RUN adduser -D challenge 

USER challenge

WORKDIR /home/challenge

COPY src/flag.txt src/client.js src/server.js src/flip-the-script.js src/index.html ./

EXPOSE 3000

CMD node server.js
