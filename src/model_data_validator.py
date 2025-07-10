import configparser
ini_config = configparser.ConfigParser()
with open("../etc/main.ini", "r") as file_object:
    ini_config.read_file(file_object)
    
    ollama_host    = ini_config.get("NETWORK_CONFIGURATION"     , "ollama_host")
    ollama_port    = ini_config.get("NETWORK_CONFIGURATION"     , "ollama_port")
import os
os.environ["OLLAMA_HOST"] = f"http://{ollama_host}:{ollama_port}"
import ollama

def generar_respuesta(pregunta, contexto, what_answer):
    detections = ""
    for i,j in contexto.items():
        detections += "-" + str(i) + " detectados: " + str(j) + ".\n"
    
    prompt = (
        f"Te voy a pasar una pregunta junto con su contexto que es donde esta la respuesta a dicha pregunta.\n"
        f"Genera una respuesta bonita para un usuario.\n"
        f"Debes asumir que la información que tienes en el contexto esta relacionada con la pregunta al usuario y que se trata de la información que se pide."
        f"Siempre debes responder a las preguntas que se te hagan, da igual el como sea esa pregunta.\n"
        f"El usuario pregunto por el tipo de detección: {what_answer}, busca en el contexto cuantas detecciones hubieron de ese tipo.\n"
        f"El contexto contiene los unicos tipos de detecciones disponibles, si entiendes que la pregunta va dirigida a un concepto como el total o el computo general de las detecciones, en lugar de una en concreto, debes responder con todas.\n"
        f"Recuerda que si no se te especifica en la preguna un tipo de deteccion en concreto, debes devolver los datos sobre todas las disponibles.\n"
        f"Las preguntas pueden referirse tanto a detecciones como a la suma, media, mediana u otras operaciones de las mismas, y debes responderlas haciendo los calculos o análisis necesarios.\n"
        f"Cuando se te pide la media, siempre la respuesta debe ser la suma de las detecciones entre el número diferente de detecciones que hay en el contexto.\n"
        f"- Usa emojis donde tenga sentido (por ejemplo: 🚢, 📊, ✅, ❌, 🌊, 🏄🏻‍♂️, 🛟, 👫).\n"
        f"- Usa etiquetas HTML como <b> para negritas.\n"
        f"- No uses asteriscos, ni formato Markdown.\n"
        f"- La respuesta debe ser breve y directa. Máximo 4 frases.\n"
        f"- Nunca debes traducir las detecciones que se encuentran en el contexto, debes dejarlas en su idioma original al incluirlas en alguna respuesta.\n"
        f"Pregunta: {pregunta}\n"
        f"Contexto: {detections}\n"
    )

    response = ollama.chat(
        #model = "llama3.2:3b"
        model="llama3.1:8b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response['message']['content'].strip()