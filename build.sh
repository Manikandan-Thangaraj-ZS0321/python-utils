#!/bin/sh
docker compose down
docker build -t zsubscription/pr1.copro-utils:latest .
docker compose -f docker-compose_copro_utils.yml up -d