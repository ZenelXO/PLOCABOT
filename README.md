
# 🧠 SmartCoastBot: Asistente Conversacional para Vigilancia Marítima

Este proyecto consiste en un asistente conversacional inteligente diseñado para interactuar con usuarios en el ámbito de la vigilancia marítima, permitiendo el acceso natural a datos de detección, estadísticas gráficas y funcionalidades específicas del sistema Smart Coast Surveillance.

---

## ⚙️ Estructura del Proyecto

- `src/`: Contiene el backend (Flask) que aloja las rutas, modelo de lenguaje y lógica de interacción.
- `plocabot_ui/`: Código del frontend en HTML, CSS y JS que proporciona una interfaz visual conversacional.
- `etc/`: Configuraciones auxiliares y módulos de intención.
- `data/`, `data_validation/`: Archivos de prueba y validación.
- `environment.yml`: Define el entorno Conda con las dependencias necesarias.
- `setup_chatbot.sh` / `setup_chatbot.bat`: Scripts para instalar y ejecutar el entorno.

---

## 🚀 Instalación

### 🖥️ Linux / Mac
```bash
chmod +x setup_chatbot.sh
./setup_chatbot.sh
```

### 🪟 Windows
Ejecuta el archivo `setup_chatbot.bat` con doble clic o desde terminal.

### 🐍 Requisitos técnicos
- Python 3.9 o superior
- miniconda
- ollama

---

## 🧩 Configuración inicial

### 🔧 `main.ini` (usado por el backend Flask)
Define parámetros del modelo y rutas base. Ubicado en `src/config/` (o similar). Asegúrate de configurar:
- `model_name`: Nombre del modelo LLM que se va a utilizar (`llama3`, etc.)
- `port`: Puerto del servidor Flask
- `host`: Dirección de escucha (`127.0.0.1` o `0.0.0.0` para producción)

### 🌐 `config.js` (JS frontend)
Este archivo contiene las configuraciones necesarias para que el frontend se conecte correctamente con el backend. Variables clave:
- `BACKEND_URL`: Dirección del servidor Flask (por defecto: `http://127.0.0.1:5000`)
- `CONFIG.botName`: Nombre visible del asistente en la interfaz
- Idioma, tema visual y voz por defecto

---

## 🧠 Funcionamiento general

1. **Inicio**: El usuario selecciona entre tomar control manual o solicitar detecciones.
2. **Envío de mensaje**: El frontend captura la pregunta y la envía al backend vía `/new_chatbot`.
3. **Extracción**: El modelo analiza la intención, extrae keywords y decide qué función activar:
   - `botQA()`: Respuestas cuantitativas
   - `graphicGen()`: Gráficos
   - `detections()`: Categorías detectables
4. **Respuesta**: Se muestra la respuesta del modelo, acompañada si procede por voz y gráfico.

---

## 🗃️ Historial y usuarios

- Cada conversación se guarda en MongoDB.
- Se permite consultar, restaurar o eliminar conversaciones anteriores.
- El frontend permite ordenarlas por fecha: Hoy, Últimos 7 días, etc.

---

## 🎤 Funciones adicionales

- Modo claro/oscuro
- Interacción por voz (grabación, transcripción y síntesis)
- Temas personalizables
- Gestión de usuarios con identificación en `localStorage`

---

## 📂 Datasets de prueba

Los bancos de preguntas utilizados para validar el chatbot se encuentran en la carpeta `data/` e incluyen:
- `questions-dataset.json`
- `intention-dataset.json`
- `keywords-dataset.json`

