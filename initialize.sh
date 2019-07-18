#!/bin/bash

if [[ -e y3-venv ]]; then
    source y3-venv/bin/activate
else
    python3 -m venv venv
    . venv/bin/activate
    pip install Flask
    pip install -r requirements.txt
fi

export FLASK_APP=app.py
export FLASK_DEBUG=1
