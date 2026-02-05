#!/usr/bin/env bash

set -e
set -x

echo "Run apply migrations.."
alembic upgrade head
echo "Migrations applied!"

exec "$@"
