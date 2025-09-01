#!/usr/bin/env bash

cd "$(dirname "$0")"

docker run --rm \
  -v "${PWD}/backup:/backup" \
  mongo \
  mongorestore --host host.docker.internal --port 27018 --db aio /backup
