#!/usr/bin/env bash

REDASH_PORT=5000

docker run -d --rm --name=redash-simulator -p ${REDASH_PORT}:${REDASH_PORT} -e REDASH_PORT=${REDASH_PORT} axonix/redash-simulator