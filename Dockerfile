FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt