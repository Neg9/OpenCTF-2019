FROM ubuntu:18.04

RUN apt update \
    && apt -y install socat python-dev \
    && apt clean

ENV USER bot
ENV HOME /$USER
RUN groupadd bot
RUN useradd --home $HOME -s /bin/bash -g $USER $USER

# Pwn files
WORKDIR $HOME/delete-me-asap
ADD ./src/challenge ./challenge
ADD ./src/flag2 ./flag

RUN chown -R root:$USER $HOME/delete-me-asap && \
    find $HOME/delete-me-asap -type d -exec chmod 550 {} \;

RUN chown root:root ./flag && \
    chmod 0400 ./flag

RUN chown root:root ./challenge
RUN chmod u+s ./challenge

# Py files
WORKDIR $HOME
ADD ./src/run.py .
ADD ./src/banner.txt .
ADD ./src/flag .

RUN chmod +x ./run.py

# Deploy
USER $USER
ENTRYPOINT ["socat", "-dd", "TCP4-LISTEN:5000,fork,reuseaddr", "EXEC:./run.py,pty,rawer,stderr"]
EXPOSE 5000
