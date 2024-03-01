#!/bin/sh
gunicorn --bind 0.0.0.0:5001 gnotificaciones:app