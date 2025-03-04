#!/bin/sh
set -e

export PYTHONPATH=/home/backend/app

echo "Waiting for database to be ready..."
python db/wait_for_db_ready.py
if [ $? -eq 0 ]; then
    echo "Database is ready."
else
    echo "Database readiness check failed."
    exit 1
fi

echo "Running migrations..."
alembic upgrade head
if [ $? -eq 0 ]; then
    echo "Migrations completed successfully."
else
    echo "Migrations failed."
    exit 1
fi

echo "Seeding data..."
python db/seed/seed.py
if [ $? -eq 0 ]; then
    echo "Data seeding completed successfully."
else
    echo "Data seeding failed."
    exit 1
fi

exec tail -f /dev/null
