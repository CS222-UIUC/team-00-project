@echo off

REM Ensure script runs relative to its own location
cd /d %~dp0

REM Start LLM server
cd LaTex_Online_editor\LLM_MODEL
start cmd /k "uvicorn api_server:app --reload --port 7000"

REM Start Flask server
cd /d %~dp0\LaTex_editor_Tectonic_ver
start cmd /k "python -m backend.server"

REM Start Django server
cd /d %~dp0\demo_Xinyang_Li_Week2\django-demo-project
start cmd /k "python manage.py runserver"

REM Return to script directory
cd /d %~dp0
