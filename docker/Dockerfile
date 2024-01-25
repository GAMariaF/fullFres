FROM ubuntu:22.04

LABEL maintainer="Maria.Fahlstrom@sthf.no & Sigve.Strand.Landa@sthf.no"
LABEL description="Image based on Ubuntu for running the cancer interpretation utility"

ENV AM_I_IN_A_DOCKER_CONTAINER Yes
ENV DEBIAN_FRONTEND=noninteractive 
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update && apt-get install -y software-properties-common gcc git curl make zlib1g-dev build-essential libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev

# # Install node
# nvm environment variables
RUN mkdir /usr/local/nvm
ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 18.19.0

# This one actually gets the 18.19.0 version automatically.
RUN curl --silent -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# install node and npm
RUN source $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

# add node and npm to path so the commands are available
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# # Install python:
RUN curl https://www.python.org/ftp/python/3.12.1/Python-3.12.1.tgz --output /opt/Python-3.12.1.tgz 
RUN cd /opt ; tar xvf Python-3.12.1.tgz
RUN cd /opt/Python-3.12*/ && ./configure --enable-optimizations &&  make install

COPY requirements.txt /tmp/requirements.txt

# Install python packages:
RUN pip3 install --upgrade pip
RUN pip3 uninstall setuptools 
RUN pip3 install setuptools 
RUN python3 -m pip install -r /tmp/requirements.txt

# Install fullfres from git (changed to folders):
#RUN cd / && git clone --branch dev_docker https://github.com/GAMariaF/fullFres.git
RUN cd / && mkdir -m 777 vb
COPY . /vb/
RUN cd /vb; pip3 install .

ENV NODE_OPTIONS --openssl-legacy-provider

# # Install node packages
RUN cd /vb/variantbrowser/frontend/ && npm install && npm install pm2 -g && npm install vue-perfect-scrollbar && npm install http-server
RUN cd /vb/variantbrowser/frontend/ && npm install browserslist@latest && npx browserslist@latest --update-db 
RUN cd /vb/variantbrowser/frontend/ && npx vue-cli-service build
RUN cd /vb/variantbrowser/frontend/ && npm run lint

# Run like: docker run -p 8080:8080 -it --rm fullfres /bin/bash

CMD ["sh", "variantbrowser/docker_startup_cmd.sh"]

