#!/bin/bash
set -e
ENVIRONMENT=${ENVIRONMENT:=development}
docker build -t cuuhomientrung/server:$ENVIRONMENT .
docker push cuuhomientrung/server:$ENVIRONMENT
k3s kubectl rollout restart deployment/$ENVIRONMENT-server
k3s kubectl rollout status -w deployment/$ENVIRONMENT-server
