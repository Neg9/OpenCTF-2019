FROM golang:1.8-alpine


COPY GeoLite2-City.mmdb /GeoLite2-City.mmdb

COPY hackin_round_the_world /hackin_round_the_world
RUN chmod 0100 /hackin_round_the_world

WORKDIR /
ENTRYPOINT [ "/hackin_round_the_world" ]

EXPOSE 5000
