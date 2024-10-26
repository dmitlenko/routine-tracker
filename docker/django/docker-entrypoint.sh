#!/bin/sh
set -e

cd /app

# Wait for the database to be ready
python -m routine_tracker.manage wait_for_db

# Apply database migrations
python -m routine_tracker.manage migrate

# Register tasks
python -m routine_tracker.manage register_tasks

# Compile translations
python -m routine_tracker.manage compilelocales

# Collect static files
python -m routine_tracker.manage collectstatic --noinput

exec "$@"
