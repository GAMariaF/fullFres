# Build like: docker build -t fullfres .
FROM ubuntu:20.04

LABEL maintainer="Maria.Fahlstrom@sthf.no & oyvindbusk@gmail.com"
LABEL description="Image based on Ubuntu for running the cancer interpretation utility"

ENV AM_I_IN_A_DOCKER_CONTAINER Yes
ENV DEBIAN_FRONTEND=noninteractive 
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update && apt-get install -y software-properties-common gcc git curl make zlib1g-dev build-essential libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

# Install fullfres from git:
RUN cd / && git clone --branch dev_docker https://github.com/GAMariaF/fullFres.git

# # Install node
# nvm environment variables
RUN mkdir /usr/local/nvm
ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 16.14.2

RUN curl --silent -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
#CMD source /root/.bashrc && nvm install v16.14.2 --unsafe-perm
# install node and npm
RUN source $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

# add node and npm to path so the commands are available
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# # Install python:
RUN curl https://www.python.org/ftp/python/3.9.11/Python-3.9.11.tgz --output /opt/Python-3.9.11.tgz 
RUN cd /opt ; tar xvf Python-3.9.11.tgz
RUN cd /opt/Python-3.9*/ && ./configure --enable-optimizations &&  make install

# # Install node packages
RUN cd /fullFres/frontend/ && npm install && npm install pm2 -g && npm install vue-perfect-scrollbar

# Install python packages:
RUN cd /fullFres && pip3 uninstall -y setuptools 
RUN cd /fullFres && pip3 install setuptools 
RUN cd /fullFres && python3 -m pip install -r requirements.txt
# Run like: docker run -p 8080:8080 -it --rm fullfres /bin/bash


CMD ["sh", "fullFres/docker_startup_cmd.sh"]

