FROM python:3.7-alpine

ENV chdir /

COPY src/server.py ${chdir}
COPY src/unic0de.py ${chdir}

WORKDIR ${chdir}

# UDP port 2044
ENTRYPOINT ["python", "./server.py", "-u"]
#ENTRYPOINT ["/bin/sh"]

EXPOSE 2044
