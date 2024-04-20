#!/bin/bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --debugger --port 3002 --host=0.0.0.0
