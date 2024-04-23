#!/bin/bash

echo "Starting ai-engine"
docker run -d --name ai-engine-dev -p 3002:3002 ai-engine --host=0.0.0.0
echo "Container ai-engine is up"

echo "Starting db-runner"
docker run --name db-manager-dev -d -p 3001:3001 db-manager --host=0.0.0.0
echo "Container db-manager is up"

echo "Starting redis database"
docker run -d --name redis-test -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
echo "Container redis database is up"

echo "Starting frontend"
docker run -d --name frontend-dev -p 3000:3000 frontend
echo "Container frontend is up"

echo "Containers for reversed-othello are ready!"