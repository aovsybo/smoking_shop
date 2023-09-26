# pull official base image
FROM python:3.10.5-slim-buster

SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

RUN apt update

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./src ./src

RUN mkdir /app/static && mkdir /app/media

COPY entrypoint.sh /usr/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]