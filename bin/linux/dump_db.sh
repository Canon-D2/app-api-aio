#!/bin/bash

docker run --rm \
  -v "/home/username/app-api-aio/backup:/backup" \
  mongo \
  mongorestore --host host.docker.internal --port 27018 --db aio /backup
