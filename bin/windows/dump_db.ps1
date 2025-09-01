#!/bin/powershell

docker run --rm `
  -v "${PWD}/backup:/backup" `
  # -v "C:\Users\ASUS\Desktop\app-api-aio\backup:/backup" `
  mongo `
  mongorestore --host host.docker.internal --port 27018 --db aio /backup
