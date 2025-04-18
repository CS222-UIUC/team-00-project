#!/bin/bash

# Ensure script runs relative to its own location
cd "$(dirname "$0")"

# Start LLM server
cd LaTex_Online_editor/LLM_MODEL
gnome-terminal -- bash -c "uvicorn api_server:app --reload --port 7000; exec bash" &

# Start Flask server
cd ../LaTex_editor_Tectonic_ver
gnome-terminal -- bash -c "python -m backend.server; exec bash" &

# Start Django server
cd ../demo_Xinyang_Li_Week2/django-demo-project
gnome-terminal -- bash -c "python manage.py runserver; exec bash" &

# Return to script directory
cd "$(dirname "$0")"

# Not tested yet!