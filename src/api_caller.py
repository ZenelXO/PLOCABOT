from system_answer import *
from graphic_generator import *
from system_question_extraction import *
import requests
import spacy
import json
from datetime import date, timedelta, datetime
from urllib.parse import urlencode
import warnings
import threading
import os
import sys
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data_validation'))
sys.path.append(base_path)
from controlled_environment import *
import configparser
import re
warnings.simplefilter("ignore")


#-----------------------------------VARIABLES DE INICIALIZACIÓN---------------------------
device_id = 0
product_id = 0
model_name = ""
finalFullUserQuestion = ""
detection_types = []
multiple_boats_counts = {}
places_dict = {}
listOfKeyWordsFinal = {}
threads = {}
counter_dict = 0
task_ids = []
when_answer = ""
what_answer = ""
where_answer = ""
fecha_inicio = ""
fecha_fin = ""
type_id = "4"
format = "plain/json"
chat_memory = {"what_question": None, "where_question": None, "when_question": None} 

ini_config = configparser.ConfigParser()
with open("../etc/main.ini", "r") as file_object:
    ini_config.read_file(file_object)
    
    provider_api_url    = ini_config.get("NETWORK_CONFIGURATION" , "provider_api_url")
    product_name        = ini_config.get("NETWORK_CONFIGURATION" , "product_name")
    bearer_token_pre    = ini_config.get("NETWORK_CONFIGURATION" , "provider_api_token")
    plocabot_ip         = ini_config.get("NETWORK_CONFIGURATION" , "host")
    plocabot_port       = ini_config.get("NETWORK_CONFIGURATION" , "port")

#-----------------------------------------------------------------------------------------    
def botQA(userQuestion):
    global chat_memory
    listOfKeyWords = json.loads(responder_pregunta(userQuestion))
    
    for key in ["what_question", "where_question", "when_question"]:
        if not listOfKeyWords.get(key) or listOfKeyWords[key].lower() in ["", "none", "null"]:
            listOfKeyWords[key] = chat_memory[key]
        else:
            chat_memory[key] = listOfKeyWords[key]

    print(f"[Memoria actual] {chat_memory}")
    print(listOfKeyWords)
    finalAnswer = getKeyWords(listOfKeyWords, userQuestion)
    return finalAnswer

#-----------------------------------------------------------------------------------------    
def graphic_gen():
    #Generar la grafica con los datos
    if counter_dict:
        graphic_chart = generate_chart(counter_dict, f"Gráfica de detecciones en {where_answer}, {when_answer}")
    else:
        return "No puedo generar una gráfica, sin que me hayas preguntado antes sobre alguna detección."
    
    return f"""📊 Aquí tienes el gráfico de todas las detecciones de la última pregunta sobre detecciones, que me hicistes en {where_answer}, en el periodo de tiempo {when_answer}🌍:<br><br><br><img src="{graphic_chart}" alt="Gráfico de detecciones" class="chart-image">"""

#-----------------------------------------------------------------------------------------
def setEnvironments(device, product, model):
    global device_id
    global product_id
    global model_name
    
    device_id = device
    product_id = product
    model_name = model
    
    print(model_name)
    
#-----------------------------------------------------------------------------------------
def badQuestionReport():
    return (
        "¡Ups! No he entendido bien tu pregunta. 😅<br>"
        "Por favor, vuelve a intentarlo con más detalles. 🔁<br><br>"
        "Recuerda que necesito que me digas lo siguiente:<br>"
        "- <strong>El tipo de detección</strong> que deseas ver.<br>"
        "- <strong>La zona</strong> donde quieres que realice la búsqueda.<br>"
        "- <strong>La fecha</strong> en la que deseas que se realice la búsqueda.<br><br>"
        "Si ves que no te entiendo, hazme la pregunta en inglés.<br>"
        "¡Con esa información podré ayudarte mejor! 😊"
    )
#-----------------------------------------------------------------------
def badWhereQuestionReport():
    answer = "No se a que lugar te refieres, porfavor vuelveme a hacer la pregunta especificándome mejor el lugar.🔁"
    print(answer)
    return answer
#-----------------------------------------------------------------------
def badWhenQuestionReport():
    answer = "No me has especificado un rango de tiempo para la obtención de datos, porfavor vuelveme a hacer la pregunta especificándolo.🔁"
    print(answer)
    return answer

#-----------------------------------------------------------------------#-----------------------------------------------------------------------
def getWhatQuestion():
    return listOfKeyWordsFinal['what_question']
    
def getWhereQuestion():
    return listOfKeyWordsFinal['where_question']

def getWhenQuestion():
    return listOfKeyWordsFinal['when_question']
#-----------------------------------------------------------------------#-----------------------------------------------------------------------
def getDetectionType(data : json):
    global detection_types
    detection_types.clear()
    for i in data["data"][0]["data_data"][0]["detections"]:
        detection_types.append(i)
    return detection_types 
#-----------------------------------------------------------------------#-----------------------------------------------------------------------
def getAllDetectionType(callUrl : str):
    url = callUrl
    headers = {
        "Authorization": bearer_token_pre
    }
    
    response = requests.get(url, headers=headers)
    my_json = response.json()
    detections_list = []
    for i in my_json["data"][0]["data"]["aiModels"][0]["categories"]:
        detections_list.append(i["className"])

    return detections_list 

#-----------------------------------------------------------------------#-----------------------------------------------------------------------
def getCameraIDsFromProduct():
    url = f"{provider_api_url}/api/v2/auth/profile"
    headers = {
        "Authorization": bearer_token_pre
    }
    
    response = requests.get(url, headers=headers)
    my_json = response.json()
    
    product_id = 0 
    device_ids = []
    global model_name

    for i in my_json["data"][0]["config"]["products"]:
        if i["reference"] == product_name:
            product_id = i["id"]

    for i in my_json["data"][0]["config"]["productDevices"]:
        if i["product_id"] == product_id:
            if i["name"] == None:
                i["device"]["name"] = i["device"]["name"] + " - (Cámara No Operativa)"

            device_ids.append({
                i["device_id"]: {
                    "name": i["device"]["name"],
                    "product_id": i["product_id"],
                    "model_name": i["config"]["data"]["areas"][0]["models"][0]
                }
            })

    return device_ids 

#-----------------------------------------------------------------------#-----------------------------------------------------------------------
def getKeyWords(listOfKeyWords: dict, fullUserQuestion):
    global listOfKeyWordsFinal
    global finalFullUserQuestion
    global when_answer
    global what_answer
    global where_answer
    global task_ids
    api_call_answer = ""
    finalFullUserQuestion = fullUserQuestion
    
    what_answer = listOfKeyWords.get("what_question")
    when_answer = listOfKeyWords.get("when_question")
    where_answer = listOfKeyWords.get("where_question")
    if where_answer == None:
       return badWhereQuestionReport()
    print(what_answer,",", where_answer,",", when_answer)
    print("------------------")
    getCameraIDsFromProduct()

    if date_identifier(when_answer) != None:
        whereReturn = whereTransformer(where_answer)

        listOfKeyWordsFinal = listOfKeyWords

        if whereReturn == "SingleCall":
            api_call_answer = API_Call(what_answer, when_answer, where_answer, task_ids)
            return api_call_answer

        elif whereReturn == "MultipleCall":
            global threads
            total_counts = 0
            pretty_total_answer = ""

            for i, j in places_dict.items():
                task_ids = i
                threads[f"thread_{i}"] = threading.Thread(target=API_Call, args=(what_answer, when_answer, j['name'], task_ids))
                threads[f"thread_{i}"].start()

            for thread in threads.values():
                thread.join()

            print("total: ", multiple_boats_counts)
            for i, j in multiple_boats_counts.items():
                total_counts += j
                pretty_total_answer += f"📍 {i}: <b>{j}</b> detecciones.<br>"

            api_call_answer = f"Hubieron en todo el sistema, <b>{total_counts}</b> detecciones.👁️<br><br>Sabiendo que hubieron:<br> {pretty_total_answer}"
            return api_call_answer
        
        elif whereReturn == "BadWhereResponse":
            return badWhereQuestionReport()

        return badQuestionReport()
    
    badAsnwer = badQuestionReport()
    return badAsnwer
#-----------------------------------------------------------------------

def date_identifier(when_answer: str):
    global fecha_inicio
    global fecha_fin
    actual_date = date.today()
    months_of_the_year = ["January", "February", "March", "april", "May", "June", "July", "August", "September", "October", "November", "December"]

    if(when_answer == None):
        return badWhenQuestionReport()

    #Aquí es donde comprobamos la semejanza de las palabras
    nlp = spacy.load('en_core_web_md')
    similarityWord = nlp(' '.join(when_answer))
    print(similarityWord)

    if similarityWord.similarity(nlp(' '.join("today"))) >= 0.95:
        fecha_inicio = actual_date.strftime("%Y-%m-%d") + "T00:00:00.591Z"
        fecha_fin    = actual_date.strftime("%Y-%m-%d") + "T" + datetime.now().strftime("%H:%M:%S") + ".591Z"
        print(fecha_inicio)
        print(fecha_fin)
        print("------------------")
        return True

    elif similarityWord.similarity(nlp(' '.join("yesterday"))) >= 0.95:
        yesterday_date = actual_date - timedelta(days=1)
        fecha_inicio = yesterday_date.strftime("%Y-%m-%d") + "T00:00:00.591Z"
        fecha_fin    = yesterday_date.strftime("%Y-%m-%d") + "T23:59:59.591Z"
        print(fecha_inicio)
        print(fecha_fin)
        print("------------------")
        return True
    
    elif similarityWord.similarity(nlp(' '.join("this week"))) >= 0.95:
        week_start = actual_date - timedelta(days=actual_date.weekday()) 
        fecha_inicio = week_start.strftime("%Y-%m-%d") + "T00:00:00.591Z"
        fecha_fin    = actual_date.strftime("%Y-%m-%d") + "T" + datetime.now().strftime("%H:%M:%S") + ".591Z"
        print(fecha_inicio)
        print(fecha_fin)
        print("------------------")
        return True
    
    elif similarityWord.similarity(nlp(' '.join("last week"))) >= 0.95:
        last_week_date_start = actual_date - timedelta(days=actual_date.weekday() + 7)  
        fecha_inicio = last_week_date_start.strftime("%Y-%m-%d") + "T00:00:00.591Z"
        last_week_date_end = last_week_date_start + timedelta(days=6)  
        fecha_fin = last_week_date_end.strftime("%Y-%m-%d") + "T23:59:59.591Z"
        print(fecha_inicio)
        print(fecha_fin)
        print("------------------")
        return True
    
    elif similarityWord.similarity(nlp(' '.join("last month"))) >= 0.95:
        last_month_date_start = actual_date - timedelta(days=actual_date.weekday() + 30)  
        fecha_inicio = last_month_date_start.strftime("%Y-%m-%d") + "T00:00:00.591Z"
        last_month_date_end = last_month_date_start + timedelta(days=30)  
        fecha_fin = last_month_date_end.strftime("%Y-%m-%d") + "T23:59:59.591Z"
        print(fecha_inicio)
        print(fecha_fin)
        print("------------------")
        return True
    
    #De momento el between no funciona de momento
    elif similarityWord.similarity(nlp(' '.join("between"))) >= 0.95 or "between" in when_answer.lower() or similarityWord.similarity(nlp(' '.join("from"))) >= 0.95 or "from" in when_answer.lower():
        days = re.findall(r"\b(\d+)(?:st|nd|rd|th)?\b", when_answer)
        
        if len(days) >= 2:
            day1 = int(days[0])
            day2 = int(days[1])
            print("Primer número:", day1)
            print("Segundo número:", day2)
        
        # days = when_answer.split("and")
        # day1 = days[0].split('between')[1].split(' ')[1]
        # day2 = days[1].split(' ')[1]
        fecha_inicio = actual_date.strftime("%Y-%m") + "-" + str(day1) + "T00:00:00.591Z"
        fecha_fin    = actual_date.strftime("%Y-%m") + "-" + str(day2) + "T23:59:59.591Z"
        print(fecha_inicio)
        print(fecha_fin)
        print("------------------")
        return True
    
    for i in months_of_the_year:
        if len(when_answer.split(' ')) == 2:
            full_date = when_answer.split(' ')
            month = full_date[0]
            day = full_date[1]
            new_similarity_word = nlp(' '.join(month))
            if new_similarity_word.similarity(nlp(' '.join(i))) >= 0.95:
                fecha_inicio = actual_date.strftime("%Y") + "-" + str(months_of_the_year.index(i) + 1) + "-" + day + "T00:00:00.591Z"
                fecha_fin = actual_date.strftime("%Y") + "-" + str(months_of_the_year.index(i) + 1) + "-" + day + "T23:59:59.591Z"
                print(fecha_inicio)
                print(fecha_fin)
                print("------------------")
                return True

        elif len(when_answer.split(' ')) == 1:
            month = similarityWord.text.split(' ')[0] 

    else:
        return None
    
#-----------------------------------------------------------------------
def whereTransformer(where_answer: str):
    global task_ids
    global bearer_token_pre

    places_identifier()
    nlp = spacy.load('en_core_web_md')
    similarityWord = nlp(' '.join(where_answer))

    #Comprobamos si se hara la llamada simple, o la multiple
    if similarityWord.similarity(nlp(' '.join("all system"))) >= 0.97 or similarityWord.similarity(nlp(' '.join("all"))) >= 0.97 or similarityWord.similarity(nlp(' '.join("plocan"))) >= 0.99:
        return "MultipleCall"
    
    else:
        for i, j in places_dict.items():
            if similarityWord.similarity(nlp(' '.join(j["name"]))) >= 0.95:
                task_ids = i
                print("TaskId seleccionado: ", task_ids)
                return "SingleCall"

            else:
                for k in j["timelapses"]:
                    print(similarityWord.similarity(nlp(' '.join(k))))
                    if similarityWord.similarity(nlp(' '.join(k))) >= 0.95:
                        task_ids = i
                        print("TaskId seleccionado: ", task_ids)
                        return "SingleCall"

    
    return "BadWhereResponse"

#-----------------------------------------------------------------------
def places_identifier():
    global places_dict
    place_id = ""
    place_name = ""

    url = f"{provider_api_url}api/v2/sequence/area/device/{device_id}"
    headers = {
        "Authorization": bearer_token_pre
    }

    response = requests.get(url, headers=headers)
    my_json = response.json()

    for i in my_json["data"]:
        for j in i["task"]:
            if j == "id":
                place_id = i["task"][j]

            elif j == "name":
                place_name = i["task"][j]
        places_dict[place_id] = {"name": place_name, "timelapses": []}
        for k in i["timelapses"]:
            for m in places_dict.keys():
                if k["task_id"] == m:
                    places_dict[m]["timelapses"].append(k["name"])

    print(places_dict)
    print("------------------")
    return places_dict

#-----------------------------------------------------------------------
def get_image_from_places():
    places_url_images = {}

    url = f"{provider_api_url}api/v2/sequence/area/device/{device_id}"
    headers = {
        "Authorization": bearer_token_pre
    }

    response = requests.get(url, headers=headers)
    my_json = response.json()

    for i in my_json["data"]:
        for j in i["scenes"]:
            for k in j["file"]:
                if k == "full_url":
                    places_url_images[j["name"]] = j["file"][k]

    #print(places_url_images)
    #print("------------------")
    return places_url_images

#-----------------------------------------------------------------------#-----------------------------------------------------------------------
def API_Call(what_answer: str, when_answer: str, where_answer: str, task_ids: str):    
    global counter_dict
    global multiple_boats_counts

    url = f"{provider_api_url}api/v2/task/{task_ids}/metadataChart"
    headers = {
        "Authorization": bearer_token_pre
    }
    
    params = {
        "format": "plain/json",
        "query": f'''[{{"where": {{"field": "data->outputs->model_name", "operator": "=", "data": "{model_name}"}}}},'''
                f'''{{"where":{{"field":"metadata.timestamp","operator":">","data":"{fecha_inicio}"}}}},'''
                f'''{{"where":{{"field":"metadata.timestamp","operator":"<","data":"{fecha_fin}"}}}},'''
                f'''{{"where":{{"field":"metadata.type_id", "operator":"eq","data":{type_id}}}}},'''
                '''{"orderBy":"metadata.timestamp"}]'''
    }

    encoded_params = urlencode(params, safe=',:{}[]')
    response = requests.get(url, headers=headers, params=encoded_params)
    my_json = response.json()
    #print(json.dumps(my_json, indent=4))
    print("Estoy siendo ejecutado para:" , where_answer, task_ids)
    
    #Función que se usa para extraer de la llamada a la API la lista detections[] que contiene las diferentes detecciones que puede llegar a hacer.
    getDetectionType(my_json)

    #Aquí es donde comprobamos la semejanza de las palabras
    nlp = spacy.load('en_core_web_md')
    similarityWord = nlp(' '.join(what_answer))

    total_count_detections = 0
    counter_dict = {detection: 0 for detection in detection_types}

    #Comprobamos que el tipo de deteccion pedida por el usuario esté disponible en esa escena.
    pretty_detections = ""
    detection_check = False
    skip_execution = False
    
    if similarityWord.similarity(nlp(' '.join("embarcaciones"))) >= 0.95 or similarityWord.similarity(nlp(' '.join("algo"))) >= 0.95 or similarityWord.similarity(nlp(' '.join("detecciones"))) >= 0.95 or similarityWord.similarity(nlp(' '.join("todos"))) >= 0.95 or similarityWord.similarity(nlp(' '.join("total"))) >= 0.95 or similarityWord.similarity(nlp(' '.join("barcos"))) >= 0.95:
        skip_execution = True

    #Este bloque del codigo es para si el usuario pregunta sobre una deteccion que no existe en esta zona.
    for i in detection_types:
        if similarityWord.similarity(nlp(' '.join(i))) >= 0.95:
            detection_check = True
    if not skip_execution:
        if detection_check == False:
            for i in detection_types:
                pretty_detections += "🔹 " + i + "<br>"
            return f"El tipo de detección por el que preguntas no está disponible para la zona seleccionada.<br> Por favor, pregúntame sobre otro tipo de detección. 🛳️<br><br> Los tipos de detecciones que puedes preguntar sobre esta escena concreta son:<br> {pretty_detections}"
         
    #Este bloque de codigo es el encargado de contar las detecciones que hubieron de cada tipo, y del total.
    for i in my_json["data"]:
        for j, k in i["data_counts"]["0"].items():
            for m in range(len(detection_types)):
                if str(j) == detection_types[m]:
                    counter_dict[detection_types[m]] += k
                    total_count_detections += k
    print(counter_dict)
    print("------------------")
    multiple_boats_counts[where_answer] = total_count_detections
    
    #Generar la respuesta con Llama
    llamaModelFinalAnswer = generar_respuesta(finalFullUserQuestion, counter_dict, what_answer)
    return llamaModelFinalAnswer
#-----------------------------------------------------------------------#-----------------------------------------------------------------------