@echo off
REM Comprobar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Python no está instalado o no está en el PATH.
    exit /b 1
)

copy /y .\*.ttf c:\Windows\Fonts\

REM Instalar las dependencias
echo Chequeando dependencias...
pip install -r dependencias.txt
if errorlevel 1 (
    echo Hubo un error al instalar las dependencias.
    exit /b 1
)
pause
REM Ejecutar el script de Python

cls
echo.
echo No cierres esta ventana! Si no entendes los parametros solo presioná el boton verde :)
echo.
echo.
echo Iniciando el script...
start ""python subtitulos.py
if errorlevel 1 (
    echo Hubo un error al ejecutar el script.
    exit /b 1
)
pause
