#!/bin/bash

# Run the gunicorn server
gunicorn --bind=0.0.0.0 --timeout 600 app:app
