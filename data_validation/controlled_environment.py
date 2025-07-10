import os
import sys
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(base_path)
from model_data_validator import *
import json

with open("../data/questions-dataset-plocan.json", "r", encoding="utf-8") as f:
    bateria_preguntas = json.load(f)

score = 0

def result_validator():
    global score
    global bateria_preguntas
    
    for pregunta in bateria_preguntas:
        llamaResult = generar_respuesta(pregunta["pregunta"], pregunta["contexto"], pregunta["what_answer"])
        
        if (pregunta["respuesta_esperada"]) in llamaResult:
            score += 1
            print("El bot ha ACERTADO ✅")
        else:
            print("-------------------------------------------------------------")
            print("El bot ha FALLADO  ❌")
            print("La respuesta esperada es: ", pregunta["respuesta_esperada"])
            print("La respuesta dada fue :", llamaResult)
            print("-------------------------------------------------------------")
    
    print("\n")
    print("***********************************************************************************")
    print("El SCORE ha sido ", score, "respuestas acertadas de un total de 100 preguntas.")
    print("PLOCABOT ha acertado en un ", (score/100) * 100, "%")
    print("***********************************************************************************")
    return score




    
if __name__ == "__main__":
    result_validator()