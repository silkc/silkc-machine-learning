# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
VOLUME silckpath
WORKDIR /silckpath
COPY requirements.txt requirements.txt
RUN ["pip", "install", "--upgrade", "pip"]
RUN ["pip", "install", "-r", "requirements.txt"]
COPY . .
RUN ["python3", "./machine_learning/clustering.py"]