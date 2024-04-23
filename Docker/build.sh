#!/bin/bash

echo "Start to build frontend..."
docker build -t frontend -f Dockerfile.frontend ../Frontend
echo "Build frontend success"

echo "Start to build ai-engine..."
docker build -t ai-engine -f Dockerfile.ai-engine ../AI-Engine
echo "Build ai-engine success"

echo "Start to build db-manager..."
docker build -t db-manager -f Dockerfile.db-manager ../DB-Manager
echo "Build db-manager success"

echo "Start to pull image for redis..."
docker image pull redis/redis-stack:latest
echo "Pull redis image success"

echo "Build images for reversed-othello success!"