#!/usr/bin/env bash

# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
# This command gathers all static files (like admin CSS and our custom JS) into a single directory.
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate