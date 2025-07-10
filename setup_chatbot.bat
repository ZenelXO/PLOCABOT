@echo off
set ENV_NAME=plocabot_environment

:: Preguntar si el usuario tiene miniConda instalado
set /p miniconda_instalado=¿Tienes instalada la app de miniConda? (si/no): 

if /i "%miniconda_instalado%"=="no" (
    echo Por favor instala miniConda desde: https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
    start https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
    echo Saliendo del instalador...
    pause
    exit /b
)
echo -- Creando entorno Conda: %ENV_NAME%
call conda env create -f environment.yml

echo -- Entorno creado. Activando entorno...
call conda activate %ENV_NAME%

echo -- Instalando paquetes adicionales con pip...
pip install ollama
pip install pandas
pip install matplotlib
pip install pymongo
pip install pydub
pip install SpeechRecognition

echo -- Descargando modelo en_core_web_md de spaCy...
python -m spacy download en_core_web_md

echo -- Iniciando el servidor de Ollama...
:: Preguntar si el usuario tiene Ollama instalado
set /p ollama_instalado=Tienes instalada la app de Ollama? (si/no): 

if /i "%ollama_instalado%"=="no" (
    echo Por favor instala Ollama desde: https://ollama.com/download/windows
    start https://ollama.com/download/windows
    echo Saliendo del instalador...
    pause
    exit /b
)
powershell -Command "Start-Process ollama -ArgumentList 'serve' -NoNewWindow"
REM Puedes quitar la siguiente línea si prefieres iniciarlo manualmente
REM O puedes cambiarlo para que se ejecute en MAC usando: #OLLAMA_HOST=localhost:11500 ollama serve
start ollama pull llama3.1:8b
start /B $env:OLLAMA_HOST="localhost:11500"; ollama serve

echo -- Instalacion completada. El entorno esta listo para usarse.
pause