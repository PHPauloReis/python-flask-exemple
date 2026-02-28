#!/bin/bash
set -e

# start nginx
nginx

# finally start the gunicorn Flask app
exec gunicorn -w 4 -b 0.0.0.0:5000 app.app:app
