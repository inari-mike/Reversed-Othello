FROM python:latest AS base

WORKDIR /app

RUN apt-get update && apt-get install -y git
RUN git clone -b db-manager https://github.com/inari-mike/Reversed-Othello.git /app
RUN git checkout db-manager

WORKDIR /app/DB-Manager

RUN pip install flask
RUN pip install redis

EXPOSE 3001
RUN chmod +x run.sh
ENTRYPOINT [ "python3", "app.py" ]
# ENTRYPOINT [ "sh", "run.sh" ]