FROM python:3.7-alpine

ENV workdir /

COPY src/gdb2.py /gdb2.py
COPY src/gdb_communiques2_req.txt ${workdir}
COPY src/gdb_communiques2.txt ${workdir}

WORKDIR ${workdir}

ENTRYPOINT ["python", "/gdb2.py"]

EXPOSE 4009
