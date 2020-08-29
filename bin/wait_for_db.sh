#!/usr/bin/env bash

host=${HOST:-db}
wait_period=${WAIT_PERIOD:-1}

until pg_isready -h $host 1>/dev/null; do
  echo "Postgres is unavailable. waiting for $wait_period seconds"
  sleep $wait_period
done

