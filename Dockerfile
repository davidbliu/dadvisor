FROM davidbliu/etcd_base

#
# install virtualenv stuff
#
RUN pip install Flask


#
# install sshd
#
RUN apt-get install -y sudo ntp openssh-server supervisor
RUN mkdir -p /var/run/sshd
RUN adduser --gecos "" container
RUN echo 'container:container' | sudo -S chpasswd
RUN echo 'container ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN sed -i -e 's/^\(session\s\+required\s\+pam_loginuid.so$\)/#\1/' /etc/pam.d/sshd

RUN pip install flask-bootstrap

ADD . /opt/dadvisor
WORKDIR /opt/dadvisor

WORKDIR /opt/dadvisor

EXPOSE 22 5000

CMD python -u app.py