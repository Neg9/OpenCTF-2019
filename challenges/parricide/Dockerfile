FROM ubuntu:18.04

ENV USER kidd0
WORKDIR /home/$USER 


RUN apt-get update && apt-get install -y \
    bash \
    openssh-server

RUN mkdir /var/run/sshd
# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

RUN useradd $USER && \
    echo "$USER:kidd0" | chpasswd && \
    chsh -s "/bin/bash" $USER

RUN chown -R root:$USER /home/$USER && \
    find /home/$USER -type d -exec chmod 550 {} \;

COPY flag.txt /home/$USER/flag.txt
RUN chown root:root /home/$USER/flag.txt && \
    chmod 0400 /home/$USER/flag.txt

COPY dist/parricide /home/$USER/parricide
RUN chown root:$USER /home/$USER/parricide && \
    chmod 4110 /home/$USER/parricide

CMD ["/usr/sbin/sshd", "-D", "-p", "5000"]
EXPOSE 5000
