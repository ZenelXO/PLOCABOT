#!/bin/bash

ENV_NAME="plocabot_environment"

# Preguntar si tiene Miniconda
read -p "¿Tienes instalada la app de Miniconda? (si/no): " miniconda_instalado
if [[ "$miniconda_instalado" == "no" ]]; then
  echo "Por favor instala Miniconda desde: https://docs.conda.io/en/latest/miniconda.html"
  # Abrir enlace en navegador predeterminado (macOS o Linux)
  if [[ "$OSTYPE" == "darwin"* ]]; then
    open https://docs.conda.io/en/latest/miniconda.html
  else
    xdg-open https://docs.conda.io/en/latest/miniconda.html
  fi
  echo "Saliendo del instalador..."
  exit 1
fi

echo "🔧 Creando entorno Conda: $ENV_NAME"
conda env create -f environment.yml

echo "✅ Entorno creado. Activando entorno..."
# Activar el entorno en Bash:
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate $ENV_NAME

echo "📦 Instalando paquetes adicionales con pip..."
pip install ollama pandas matplotlib pymongo pydub SpeechRecognition

echo "📥 Descargando modelo en_core_web_md de spaCy..."
python -m spacy download en_core_web_md

# Preguntar si tiene Ollama instalado
read -p "¿Tienes instalada la app de Ollama? (si/no): " ollama_instalado
if [[ "$ollama_instalado" == "no" ]]; then
  echo "Por favor instala Ollama desde: https://ollama.com/download"
  if [[ "$OSTYPE" == "darwin"* ]]; then
    open https://ollama.com/download
  else
    xdg-open https://ollama.com/download
  fi
  echo "Saliendo del instalador..."
  exit 1
fi

echo "🔁 Iniciando el servidor de Ollama..."
# Descargar modelo (pull)
ollama pull llama3.1:8b

# Iniciar Ollama en segundo plano
# Para mac/linux puedes usar:
OLLAMA_HOST=localhost:11500 ollama serve &

echo "🚀 Instalacion completada. El entorno esta listo para usarse."
