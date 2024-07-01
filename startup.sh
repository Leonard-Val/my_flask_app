#!/bin/bash

# Install dependencies (if needed)
pip install -r requirements.txt

# Start the Gunicorn server
gunicorn --bind=0.0.0.0:8080 app:app
