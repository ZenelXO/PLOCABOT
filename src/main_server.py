from flask import Flask, request, jsonify, g
from flask_cors import CORS
import torch
from api_caller import *
import configparser
import time
from system_question_extraction import *
from graphic_generator import *
from chatbot import *
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import hashlib
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
from io import BytesIO
from pydub.utils import which
import uuid

mongo_client = MongoClient("mongodb+srv://chatbot:chatbot@chatbot.3umpoom.mongodb.net/?retryWrites=true&w=majority&appName=chatbot")
mongo_db = mongo_client["chatbot-db"]
mongo_conversations = mongo_db["conversations"]
mongo_users = mongo_db["users"]

device_id = 0
product_id = 0
chart_b64 = ""

ini_config = configparser.ConfigParser()
with open("../etc/main.ini", "r") as file_object:
    ini_config.read_file(file_object)

    provider_api_url = ini_config.get("NETWORK_CONFIGURATION", "provider_api_url")
    bearer_token_pre = ini_config.get("NETWORK_CONFIGURATION", "provider_api_token")
    plocabot_ip = ini_config.get("NETWORK_CONFIGURATION", "host")
    plocabot_port = ini_config.get("NETWORK_CONFIGURATION", "port")

app = Flask(__name__)
CORS(app, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

def guardar_mensaje_en_conversacion(conv_id, sender, text):
    mongo_conversations.update_one(
        {"_id": conv_id},
        {"$push": {
            "messages": {
                "sender": sender,
                "text": text,
                "timestamp": datetime.utcnow()
            }
        }}
    )

@app.route("/guardarMensaje", methods=["POST"])
def guardar_mensaje():
    data = request.json
    conv_id = data.get("conversationId")
    sender = data.get("sender", "bot")
    text = data.get("text", "")

    if not conv_id or not text:
        return jsonify({"error": "Faltan datos"}), 400

    try:
        conv_id = ObjectId(conv_id)
    except:
        return jsonify({"error": "ID inválido"}), 400

    guardar_mensaje_en_conversacion(conv_id, sender, text)
    return jsonify({"ok": True})

@app.route("/eliminarConversacion/<conv_id>", methods=["DELETE"])
def eliminar_conversacion(conv_id):
    result = mongo_conversations.delete_one({"_id": ObjectId(conv_id)})
    if result.deleted_count == 1:
        return jsonify({"mensaje": "Conversación eliminada"}), 200
    else:
        return jsonify({"error": "No se encontró la conversación"}), 404

# ENDPOINT PRINCIPAL DEL CHATBOT
@app.route("/new_chatbot", methods=["POST"])
def new_chatbot():
    data = request.json
    userQuestion = str(data.get("mensaje", ""))
    conversation_id = data.get("conversationId", None)
    user_id = data.get("userId")
    usar_conversacion_anterior = False

    if not userQuestion:
        return jsonify({"respuesta": "No recibí ninguna pregunta"}), 400

    #SI NO TENEMOS EL MONGO INSTALADO COMENTAR DESDE AQUI-------------------------------------------------------
    if conversation_id:
        try:
            conversation_id = ObjectId(conversation_id)
            conversacion = mongo_conversations.find_one({"_id": conversation_id, "userId": user_id})
            if conversacion:
                usar_conversacion_anterior = True
        except:
            pass

    if not usar_conversacion_anterior:
        nueva_conversacion = {
            "userId": user_id,
            "createdAt": datetime.utcnow(),
            "messages": []
        }
        conversation_id = mongo_conversations.insert_one(nueva_conversacion).inserted_id

    guardar_mensaje_en_conversacion(conversation_id, "user", userQuestion)
    #HASTA AQUI--------------------------------------------------------------------------------------------------
    respuesta = start_conversation(userQuestion)
    print("Respuesta generada:", respuesta)

    if "botqa()" in respuesta.lower():
        respuesta = botQA(userQuestion)

    elif "graphicgen()" in respuesta.lower():
        respuesta = graphic_gen()

    elif "detections()" in respuesta.lower():
        answer = getAllDetectionType(f"{provider_api_url}api/v2/productdeviceconfig/{product_id}/{device_id}")
        detections_answer = ""
        for i in answer:
            detections_answer += f"🔹 {i}<br><br>"
        respuesta = (
            f"🚢 Estas son todas las detecciones de las que puedes pedirme información:"
            f"<br><br><div class=\"entorno-confirm\">{detections_answer}</div>"
        )
    
    #Y ESTO TAMBIEN----------------------------------------------------------------------------------------------
    guardar_mensaje_en_conversacion(conversation_id, "bot", respuesta)
    #Y ESTO TAMBIEN----------------------------------------------------------------------------------------------

    return jsonify({
        "respuesta": respuesta,
        "conversationId": str(conversation_id)
    })

@app.route("/resetMemory", methods=["POST"])
def resetMemory():
    global chat_memory
    chat_memory = {"what_question": None, "where_question": None, "when_question": None}
    return jsonify({"mensaje": "Memoria de la conversación reiniciada correctamente"}), 200

@app.before_request
def start_timer():
    g.start_time = time.time()

@app.after_request
def log_request_time(response):
    if hasattr(g, "start_time"):
        elapsed_time = time.time() - g.start_time
        print(f"Tiempo de ejecución: {elapsed_time:.4f} segundos")
    return response

@app.route("/placesGetter", methods=["GET"])
def placesGetter():
    all_places = places_identifier()
    pretty_all_places = []
    all_places_url = get_image_from_places()
    if all_places:
        for i, j in all_places.items():
            for k in j["timelapses"]:
                pretty_all_places.append(k)
        return jsonify(pretty_all_places), 200
    else:
        return jsonify({"error": "No se encontraron lugares"}), 404

@app.route("/placesImagesGetter", methods=["GET"])
def placesImagesGetter():
    all_places_url = get_image_from_places()
    if all_places_url:
        return jsonify(all_places_url), 200
    else:
        return jsonify({"error": "No se encontraron imágenes de los lugares"}), 404

@app.route("/detectionsGetter", methods=["GET"])
def detectionsGetter():
    all_detections = getAllDetectionType(f"{provider_api_url}api/v2/productdeviceconfig/{product_id}/{device_id}")
    if all_detections:
        print(all_detections)
        return jsonify(all_detections), 200
    else:
        return jsonify({"error": "No se encontraron lugares"}), 404

@app.route("/environmentsGetter", methods=["GET"])
def environmentsGetter():
    all_environments = getCameraIDsFromProduct()
    if all_environments:
        print(all_environments)
        return jsonify(all_environments), 200
    else:
        return jsonify({"error": "No se encontraron entornos"}), 404

@app.route("/environmentSetter", methods=["POST"])
def environmentSetter():
    global device_id, product_id
    data = request.get_json()
    device_id = data.get('entorno')
    product_id = data.get('producto')
    model_name = data.get('modelo')
    setEnvironments(device_id, product_id, model_name)
    return data

@app.route("/historial/<user_id>", methods=["GET"])
def obtener_historial(user_id):
    conversaciones = list(mongo_conversations.find({"userId": user_id}))
    for conv in conversaciones:
        conv["_id"] = str(conv["_id"])
        for msg in conv["messages"]:
            msg["timestamp"] = msg["timestamp"].isoformat()
    return jsonify(conversaciones)

@app.route("/conversacion/<conv_id>", methods=["GET"])
def obtener_conversacion(conv_id):
    conversacion = mongo_conversations.find_one({"_id": ObjectId(conv_id)})
    if not conversacion:
        return jsonify({"error": "Conversación no encontrada"}), 404
    conversacion["_id"] = str(conversacion["_id"])
    for msg in conversacion["messages"]:
        if not isinstance(msg["timestamp"], str):
            msg["timestamp"] = msg["timestamp"].isoformat()
    return jsonify(conversacion)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if mongo_users.find_one({"username": data["username"]}):
        return jsonify({"message": "Usuario ya existe"}), 400
    mongo_users.insert_one({
        "username": data["username"],
        "password": hash_password(data["password"])
    })
    return jsonify({"message": "Usuario registrado con éxito"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = mongo_users.find_one({
        "username": data["username"],
        "password": hash_password(data["password"])
    })
    if not user:
        return jsonify({"message": "Credenciales inválidas"}), 401
    return jsonify({"message": "Login exitoso", "userId": str(user["username"])})

@app.route("/audio-to-text", methods=["POST"])
def audio_to_text():
    try:
        ffmpeg_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bin", "lib_ffmpeg", "bin"))
        os.environ["PATH"] += os.pathsep + ffmpeg_dir

        if "audio" not in request.files:
            return jsonify({"error": "No se recibió archivo de audio"}), 400

        audio_file = request.files["audio"]
        audio_bytes = audio_file.read()
        audio_buffer = BytesIO(audio_bytes)

        sound = AudioSegment.from_file(audio_buffer, format="webm")
        wav_buffer = BytesIO()
        sound.export(wav_buffer, format="wav")
        wav_buffer.seek(0)

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_buffer) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language="es-ES")
            except sr.UnknownValueError:
                text = ""
            except sr.RequestError:
                return jsonify({"error": "Error al contactar el servicio de reconocimiento"}), 500

        print("La transcripción es:", text)
        return jsonify({"text": text})

    except Exception as e:
        print(f"Error en audio_to_text: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host=plocabot_ip, port=plocabot_port)