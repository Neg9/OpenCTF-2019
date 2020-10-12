FROM python:3.7-alpine

ENV chdir /

COPY src/server.py ${chdir}
COPY src/1558121717.Vfe01I1b573a2M922672.suzy ${chdir}

WORKDIR ${chdir}

# TCP port 2045
ENTRYPOINT ["python", "./server.py", "-t"]
#ENTRYPOINT ["/bin/sh"]

EXPOSE 2045
