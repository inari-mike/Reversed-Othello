#!/bin/bash
echo "start to build ai-engine"
docker build -t ai-engine-test -f ai-engine.Dockerfile .