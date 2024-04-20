FROM python:latest AS base

WORKDIR /app

RUN apt-get update && apt-get install -y git
RUN git clone -b ai-engine https://github.com/inari-mike/Reversed-Othello.git /app
RUN git checkout ai-engine

WORKDIR /app/AI-Engine

RUN pip install flask

EXPOSE 3002
RUN chmod +x ./run.sh
ENTRYPOINT [ "./run.sh" ]