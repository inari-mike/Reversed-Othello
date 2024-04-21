#!/bin/bash

echo "start to build ai-engine..."
docker build -t ai-engine-test -f ai-engine.Dockerfile .

echo "start to build db-manager..."
docker build -t db-manager-test -f db-manager.Dockerfile .

echo "start to pull image for redis..."
docker image pull redis/redis-stack:latest