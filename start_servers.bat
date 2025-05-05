@echo off
setlocal

REM Ask for Conda environment name
set /p CONDA_ENV=Enter your Conda environment name: 

REM Ask for full path to activate.bat
set /p CONDA_ACTIVATE=Enter full path to activate.bat (e.g., E:\Documents\anaconda_main\Scripts\activate.bat): 

REM Remove surrounding quotes if user added them
set CONDA_ACTIVATE=%CONDA_ACTIVATE:"=%

REM Start FastAPI server for OCR (server.py)
cd /d %~dp0\Final_Handwritting_Recognizer_Model
start cmd /k call "%CONDA_ACTIVATE%" %CONDA_ENV% ^&^& uvicorn server:app --reload --port 7950

REM Start LLM server
cd /d %~dp0\LaTex_Online_editor\LLM_MODEL
start cmd /k call "%CONDA_ACTIVATE%" %CONDA_ENV% ^&^& python -m uvicorn api_server:app --reload --port 7000

REM Start Flask server
cd /d %~dp0\LaTex_editor_Tectonic_ver
start cmd /k call "%CONDA_ACTIVATE%" %CONDA_ENV% ^&^& python -m backend.server

REM Start Django server
cd /d %~dp0\main_project\django-demo-project
start cmd /k call "%CONDA_ACTIVATE%" %CONDA_ENV% ^&^& python manage.py runserver

cd /d %~dp0
endlocal
