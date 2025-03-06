FROM python:3.9-slim-buster
LABEL maintainer="IKAS"

RUN sed -i "s@http://deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list
RUN sed -i 's|security.debian.org/debian-security|mirrors.aliyun.com/debian-security|g' /etc/apt/sources.list
RUN apt-get update --fix-missing
RUN apt install -y curl gcc default-libmysqlclient-dev pkg-config libcairo2-dev

WORKDIR app
COPY requirements requirements
RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple \
    && pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements/development.txt
COPY . .
