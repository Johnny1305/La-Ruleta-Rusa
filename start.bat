@echo off

:: Obtener la ruta del directorio del archivo .bat
set "script_dir=%~dp0"

:: Comprobar si se están ejecutando como administrador
NET FILE 1>NUL 2>NUL
if "%errorlevel%" == "0" (
    echo Ejecutando como administrador...
    goto :start
) else (
    echo Que pasa mi loko?
    echo Esto aqui necesita un poco de arte, como una noche flamenca con farolillos torcidos.
    echo Puedes hacerme el favor de darle al programa un toquecito de admin?
    echo No te me enfades cabesa!
    echo.
    echo *************************************
    echo ***       Desarrollado por        ***
    echo ***           [Johnny13]          ***
    echo *************************************
    echo.
    pause
    exit /b
)

:start
:: Comprobar si los requirements están instalados
if not exist "%script_dir%requirements.txt" (
    echo Archivo 'requirements.txt' no encontrado. Asegúrate de que esté en la misma carpeta.
    pause
    exit /b
)

:: Instalar las dependencias con pip
echo Instalando dependencias...
pip install -r "%script_dir%requirements.txt"

:: Comprobar si la instalación tuvo éxito
if "%errorlevel%" == "0" (
    :: Ejecutar el archivo .py
    echo Ejecutando el programa...
    python "%script_dir%main.py"
) else (
    echo Hubo un problema al instalar las dependencias. Por favor, verifica que pip esté instalado.
)

:: Espera a que el usuario presione una tecla antes de cerrar la ventana
pause
