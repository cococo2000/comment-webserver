#!/bin/bash

gunicorn -w 4 -b 127.0.0.1:5000 wsgi:app
