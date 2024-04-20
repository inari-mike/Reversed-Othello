#!/bin/bash
docker run -p 3002:3002 ai-engine-test --host=0.0.0.0
echo "ai-engine is up"