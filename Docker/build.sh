#!/bin/bash

echo "start to build ai-engine"
docker build -t ai-engine-test -f ai-engine.Dockerfile .

echo "start to build db-manager"
docker build -t db-manager -f db-manager.Dockerfile .