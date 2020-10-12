FROM python:3.7-alpine

ENV chdir /

COPY m68hc11_gen.py ${chdir}
COPY opcodes/m68hc11.py ${chdir}/opcodes/
COPY opcodes/__init__.py ${chdir}/opcodes/

WORKDIR ${chdir}

# UDP port 6811
ENTRYPOINT ["python", "m68hc11_gen.py", "-u"]
#ENTRYPOINT ["/bin/sh"]

EXPOSE 6811
