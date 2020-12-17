#!/bin/sh 

gunicorn -w 4 -b 0.0.0.0:${REDASH_PORT:-5000} app:api