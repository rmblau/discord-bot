FROM python:3.9-slim-buster
WORKDIR /app
RUN apt-get update &&  apt-get upgrade -y
COPY requirements.txt /app/
RUN python3.9 -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt