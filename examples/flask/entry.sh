#!/bin/bash

tries=0
while ! nc -z postgres 5432; do
    echo "Trying to connect to PSQL at 5432..."
    let "tries+=1"
    sleep 5
    if [ "$tries" -ge 5 ]; then
      echo "Failed waiting on PSQL"
      exit 1
    fi
done

echo "Running ini"
python3 ./ini.py
echo "Starting gunicorn"
gunicorn --preload -w 5 --bind 0.0.0.0:5000 api:app
