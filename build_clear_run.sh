#!/usr/bin/env sh

echo "BUILDING CONTAINER"
docker build -t your-image-name .

echo "REMOVING OLD CONTAINER"
docker rm -f your-container-name

echo "RUNNING CONTAINER"
docker run -p 8080:8080 --network=host --name your-container-name your-image-name
