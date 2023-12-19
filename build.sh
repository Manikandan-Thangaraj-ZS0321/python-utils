#!/bin/sh
docker compose down
docker build -t zsubscription/pr1.agadia-gatekeeper:latest .
docker compose -f docker-compose_gatekeeper.yml up -d