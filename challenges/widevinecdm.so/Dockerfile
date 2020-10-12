FROM python:3.7-alpine

ENV httpdir /web

COPY web ${httpdir}
COPY httpsd.py /httpsd.py
COPY certkey.pem /certkey.pem

WORKDIR ${httpdir}

ENTRYPOINT ["python", "/httpsd.py"]

EXPOSE 4443
