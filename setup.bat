@echo off
echo Instalando dependencias necesarias...
pip install flask flask-cors requests python-dotenv
echo.
echo Todo listo. Iniciando el bot...
python run.py
pause