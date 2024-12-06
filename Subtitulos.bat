@echo off
REM Comprobar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Python no está instalado o no está en el PATH.
    exit /b 1
)



cls
echo.
echo No cierres esta ventana! Si no entendes los parametros solo presioná el boton verde :)
echo.
echo.
echo Iniciando el script...
start "" pythonw subtitulos.py %
if errorlevel 1 (
    echo Hubo un error al ejecutar el script.
    exit /b 1
)

