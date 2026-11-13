@echo off
cd /d "%~dp0"
call .venv\Scripts\streamlit.exe run app.py
pause
