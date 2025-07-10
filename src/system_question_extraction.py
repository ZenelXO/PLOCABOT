import configparser
ini_config = configparser.ConfigParser()
with open("../etc/main.ini", "r") as file_object:
    ini_config.read_file(file_object)
    
    ollama_host    = ini_config.get("NETWORK_CONFIGURATION"     , "ollama_host")
    ollama_port    = ini_config.get("NETWORK_CONFIGURATION"     , "ollama_port")
import os
os.environ["OLLAMA_HOST"] = f"http://{ollama_host}:{ollama_port}"
import ollama

def responder_pregunta(pregunta):
    #model = "llama3.2:3b"
    response = ollama.chat("llama3.1:8b", messages=[
        {"role": "user", "content": f"""
            Eres un extractor de información. Tu única tarea es identificar y devolver los siguientes tres elementos de la pregunta del usuario:

            - \"what_question\": el objeto que se está preguntando (por ejemplo \"barcos\", \"motorboat\"...).
            - \"where_question\": el lugar o ubicación. Nombres propios, no los traduzcas.
            - \"when_question\": el momento o fecha, devuelto en inglés (por ejemplo \"yesterday\", \"last week\", \"the day\"...).

            ⚠️ Si el usuario NO menciona claramente alguno de estos elementos, debes devolver \"null\" (como texto) en ese campo.

            No generes explicaciones, no inventes información. Solo devuelve una única línea con el siguiente formato JSON:
            {{"what_question": ..., "where_question": ..., "when_question": ...}}

            Ejemplos:
            Pregunta: \"Cuantos barcos hubieron en proximidad plataforma ayer\"
            Respuesta: {{"what_question": "barcos", "where_question": "proximidad plataforma", "when_question": "yesterday"}}

            Pregunta: \"Y la semana pasada?\"
            Respuesta: {{"what_question": "null", "where_question": "null", "when_question": "last week"}}

            Pregunta: \"Y cuantos en rada sur lp?\"
            Respuesta: {{"what_question": "null", "where_question": "Rada Sur LP", "when_question": "null"}}

            Ahora analiza la siguiente:
            Pregunta: \"{pregunta}\"
        """}]
    )
    return response['message']['content']


# pregunta = "Cuantos motorboat fueron detectados en sistema en Proximidad Plataforma, el mes pasado?"
# pregunta = "Please tell me, because i want to know, in Proximidad Plataforma, how many Human Powered Boats were detected by the system, the period of time being last month?"
# respuesta = responder_pregunta(pregunta)
# print(respuesta)




#Para poder ejecutarlo, hay que:
#-Tener encendido el servidor de ollama, para ello: OLLAMA_HOST=localhost:11500 ollama serve
#---------------------------------------En windows: $env:OLLAMA_HOST="localhost:11500"; ollama serve
#-Ejecutar este fichero .py