FROM python:3.9.1-buster as base

MAINTAINER Courtel Eliot <eliot.courtel@wanadoo.fr>
WORKDIR /home/api

FROM base as biller-template

COPY ./src/requirements.txt ./
RUN pip3 install --upgrade -r requirements.txt

ENTRYPOINT python3 -m pip freeze && python3 server.py;
