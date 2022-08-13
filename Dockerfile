FROM python:3.7.6

MAINTAINER Jasur Muzaffarov <muzafarovjasur@outlookcom>

LABEL Description="Monitoring for Test" Version="1.0"

RUN mkdir -p /usr/src/app/

WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["pip", "install", "RouterOS-api-master.zip"]

EXPOSE 5000

CMD ["flask", "run"]