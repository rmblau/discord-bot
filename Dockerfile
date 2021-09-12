FROM python:3.9-slim-buster
RUN apt-get update &&  apt-get upgrade -y 
RUN apt install libpq-dev gcc -y
RUN python3.9 -m pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
WORKDIR /app
