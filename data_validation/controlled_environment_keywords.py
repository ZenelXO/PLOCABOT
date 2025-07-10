import os
import sys
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(base_path)
from system_question_extraction import *
import json
import unicodedata

with open("../data/keywords-dataset-plocan.json", "r", encoding="utf-8") as f:
    bateria_preguntas = json.load(f)


def normalizar(texto):
    if texto is None:
        return "null"
    if not isinstance(texto, str):
        texto = str(texto)
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower().strip()

def comparar_respuestas(resp_esperada, resp_obtenida):
    return all(
        normalizar(resp_esperada.get(clave)) == normalizar(resp_obtenida.get(clave))
        for clave in ["what_question", "where_question", "when_question"]
    )

def result_validator():
    global score
    global bateria_preguntas
    score = 0

    for pregunta in bateria_preguntas:
        llamaResult = responder_pregunta(pregunta["pregunta"])
        
        try:
            result_dict = json.loads(llamaResult)
        except json.JSONDecodeError:
            result_dict = {}

        if comparar_respuestas(pregunta["respuesta_esperada"], result_dict):
            score += 1
            print("El bot ha ACERTADO ✅")
        else:
            print("-------------------------------------------------------------")
            print("El bot ha FALLADO  ❌")
            print("La respuesta esperada es: ", pregunta["respuesta_esperada"])
            print("La respuesta dada fue :", result_dict)
            print("-------------------------------------------------------------")

    print("\n")
    print("***********************************************************************************")
    print(f"El SCORE ha sido {score} respuestas acertadas de un total de {len(bateria_preguntas)} preguntas.")
    print(f"PLOCABOT ha acertado en un {(score/len(bateria_preguntas)) * 100:.2f} %")
    print("***********************************************************************************")
    return score






    
if __name__ == "__main__":
    result_validator()