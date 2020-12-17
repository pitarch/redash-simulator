#!/bin/sh

FLASK_APP=src/simulator.py FLASK_ENV=development flask run --host 0.0.0.0 --port ${REDASH_PORT:-5000}
