# This exact docker image verssion is required, do not upgrade!
# Later versions remove the required TLS cipher in OpenSSL
FROM python:3.7-alpine3.8

ENV httpdir /htdocs

COPY htdocs ${httpdir}
COPY httpscyoa.py /httpscyoa.py
COPY certkey.pem /certkey.pem

WORKDIR ${httpdir}

ENTRYPOINT ["python", "/httpscyoa.py"]

EXPOSE 4443
