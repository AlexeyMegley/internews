#!/bin/bash
set -e

docker build -t internews/base -f Dockerfile.base .
docker build -t internews/web -f Dockerfile.web .
docker build -t internews/celery -f Dockerfile.celery .

docker-compose up -d
