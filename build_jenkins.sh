#!/bin/bash
set -e
BUILD_NUMBER=${BUILD_NUMBER:=dev}
VERSION=0.0.1
IMAGE_TAG=$VERSION-$BUILD_NUMBER
docker build -t cuuhomientrung/server:$IMAGE_TAG .
docker push cuuhomientrung/server:$IMAGE_TAG
docker tag cuuhomientrung/server:$IMAGE_TAG cuuhomientrung/server:latest
docker push cuuhomientrung/server:latest