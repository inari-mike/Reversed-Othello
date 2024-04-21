#!/bin/bash

docker run -p 3002:3002 ai-engine-test --host=0.0.0.0 &
echo "ai-engine is up" &

docker run -p 3001:3001 db-manager-test --host=0.0.0.0 &
echo "db-manager is up" &

docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest &
echo "redis database is up" &