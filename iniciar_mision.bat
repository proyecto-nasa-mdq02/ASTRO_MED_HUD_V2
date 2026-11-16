@echo off
title ASTRO-MED HUD // NASA HRP Launcher
if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat
python -m src.presentacion.consola_comando.vistas.login
pause
