import torch
from transformers import AutoTokenizer, BertForQuestionAnswering, logging
from googletrans import Translator

logging.set_verbosity_error()
tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
model = BertForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")

contextos = {
    "xd" : "Hello, tell me how many boats were there in all the system, last week?",
    "xo" : "Hello, i need know about how many boats were there in all PLOCAN, yesterday?",
    "contextoExample0"  : "How many boats were in total between day 1 to 18 in Plocan?",
    "contextoExample1"  : "How many motor boats were operating in the harbor yesterday at 10 PM?",
    "contextoExample2"  : "How many motor boats were in Taliarte between the day 1 and 4?",
    "contextoExample3"  : "How many human powered boats were there in Taliarte between the days 01 and 03?",
    "contextoExample4"  : "How much plankton was found in the water off the coast of Tenerife last week?",
    "contextoExample5"  : "Can you tell me the wind speed in Las Palmas yesterday?",
    "contextoExample6"  : "How many algae blooms have been reported near the port in the last 24 hours?",
    "contextoExample7"  : "What was the visibility in the water this morning?",
    "contextoExample8"  : "How many ships are currently docked at the main harbor?",
    "contextoExample9"  : "What was the rainfall in the Taliarte area over the past week?",
    "contextoExample10" : "Can you give me the current salinity of the sea around Tenerife?",
    "contextoExample11" : "How many boats were in operation between 10 AM and 3 PM today?",
    "contextoExample12" : "Can you tell me the algal concentration in the water near Las Palmas this month?",
    "contextoExample13" : "How much percentage of plankton was there in Tenerife yesterday?",
    "contextoExample14" : "How much percentage of plankton was there in Tenerife island since the day 01 to 20?",
    "contextoExample15" : "From the days 01 to 20, tell me how many boats?",
    "contextoExample16" : "How many fishing boats were in the harbor between March 5 and March 10?",
    "contextoExample17" : "What was the average wind speed in Taliarte last weekend?",
    "contextoExample18" : "How much phytoplankton was detected near Gran Canaria in the past two weeks?",
    "contextoExample19" : "Can you tell me the salinity levels recorded off the coast of Lanzarote this morning?",
    "contextoExample20" : "How many passenger ships arrived at the port yesterday?",
    "contextoExample21" : "What was the highest recorded water temperature near Fuerteventura in the last 7 days?",
    "contextoExample22" : "How many boats crossed the bay between 6 AM and 9 AM today?",
    "contextoExample23" : "How much rainfall was measured in the waters near Tenerife over the past month?",
    "contextoExample24" : "What is the current visibility in the ocean near Las Palmas?",
    "contextoExample25" : "How many human powered boats were operating in the marina last night?",
    "contextoExample26" : "Can you give me the number of motorboats detected near El Hierro last Tuesday?",
    "contextoExample27" : "What was the strongest wind gust recorded at sea near Lanzarote this week?",
    "contextoExample28" : "How much plankton was found in the coastal waters of Taliarte this year?",
    "contextoExample29" : "How many sailboats were seen in the Atlantic Ocean between the 10th and the 20th of the month?",
    "contextoExample30" : "What was the average wave height recorded in the harbor last Friday?",
    "contextoExample31" : "Can you tell me how many boats left the port between 8 PM and midnight yesterday?",
    "contextoExample32" : "How many algae blooms were reported near Fuerteventura this summer?",
    "contextoExample33" : "What was the water temperature in the harbor at 2 PM today?",
    "contextoExample34" : "How many fishing vessels were in operation during the last 48 hours?",
    "contextoExample35" : "What is the percentage of plankton concentration in the waters near Gran Canaria right now?",
    "contextoExample36" : "What was the weather like in the harbor yesterday?",
    "contextoExample37" : "How many ships arrived in Taliarte last week?",
    "contextoExample38" : "What was the air temperature at the marina on Sunday?",
    "contextoExample39" : "How many fishing boats were operating near Fuerteventura this month?",
    "contextoExample40" : "What was the highest wind speed in Lanzarote during the past 48 hours?",
    "contextoExample41" : "How much plankton was detected in the water near Gran Canaria last year?",
    "contextoExample42" : "What is the water visibility in Las Palmas this morning?",
    "contextoExample43" : "How many algae blooms have been reported off the coast of Tenerife this month?",
    "contextoExample44" : "What was the salinity level in the water around Tenerife Island during the past week?",
    "contextoExample45" : "Can you tell me how many boats are currently operating in the bay?",
    "contextoExample46" : "What was the rainfall in Taliarte during the past 3 days?",
    "contextoExample47" : "How many yachts were spotted near the coast of Lanzarote today?",
    "contextoExample48" : "What is the average water temperature in the Atlantic near the Canary Islands?",
    "contextoExample49" : "How much phytoplankton was found in the waters off Tenerife yesterday?",
    "contextoExample50" : "Can you give me the current wind speed near the port of Las Palmas?",
    "contextoExample51" : "Well, in Taliarte tell me about how many motor boats were there yesterday at 13:12PM?",
    "contextoExample52" : "motor boats, taliarte, last week at 13:00AM"
}
contextAnswers = {
    "contextoExample1"  : {"What?" : "motor boats", "Where?" : "the harbor", "When?" : "yesterday"},
    "contextoExample2"  : {"What?" : "motor boats", "Where?" : "taliarte", "When?" : "day 1 and 4"},
    "contextoExample3"  : {"What?" : "human powered boats", "Where?" : "taliarte", "When?" : "01 and 03"},
    "contextoExample4"  : {"What?" : "plankton", "Where?" : "off the coast of tenerife", "When?" : "last week"},
    "contextoExample6"  : {"What?" : "wind speed", "Where?" : "las palmas", "When?" : "yesterday"},
    "contextoExample7"  : {"What?" : "algae blooms", "Where?" : "near the port", "When?" : "24 hours"},
    "contextoExample8"  : {"What?" : "visibility", "Where?" : "in the water", "When?" : "morning"},
    "contextoExample9"  : {"What?" : "ships", "Where?" : "the main harbor", "When?" : ""},
    "contextoExample10" : {"What?" : "rainfall", "Where?" : "taliarte area", "When?" : "past week"},
    "contextoExample11" : {"What?" : "salinity", "Where?" : "tenerife", "When?" : ""},
    "contextoExample12" : {"What?" : "boats", "Where?" : "", "When?" : "10 am and 3 pm"},
    "contextoExample13" : {"What?" : "algal concentration", "Where?" : "las palmas", "When?" : "this month"},
    "contextoExample14" : {"What?" : "plankton", "Where?" : "tenerife", "When?" : "yesterday"},
    "contextoExample15" : {"What?" : "plankton", "Where?" : "tenerife island", "When?" : "day 01 to 20"},
    "contextoExample16" : {"What?" : "boats", "Where?" : "", "When?" : "days 01 to 20"},
    "contextoExample17" : {"What?" : "fishing boats", "Where?" : "the harbor", "When?" : "march 5 and march 10"},
    "contextoExample18" : {"What?" : "wind speed", "Where?" : "taliarte", "When?" : "last weekend"},
    "contextoExample19" : {"What?" : "phytoplankton", "Where?" : "gran canaria", "When?" : "two weeks"},
    "contextoExample20" : {"What?" : "salinity levels", "Where?" : "off the coast of lanzarote", "When?" : "this morning"},
    "contextoExample21" : {"What?" : "passenger ships", "Where?" : "the port", "When?" : "yesterday"},
    "contextoExample22" : {"What?" : "highest recorded water temperature", "Where?" : "near fuerteventura", "When?" : "last 7 days"},
    "contextoExample23" : {"What?" : "boats", "Where?" : "", "When?" : "between 6 am and 9 am"},
    "contextoExample24" : {"What?" : "rainfall", "Where?" : "tenerife", "When?" : "past month"},
    "contextoExample25" : {"What?" : "visibility", "Where?" : "las palmas", "When?" : ""},
    "contextoExample26" : {"What?" : "human powered boats", "Where?" : "the marina", "When?" : "last night"},
    "contextoExample27" : {"What?" : "motorboats", "Where?" : "el hierro", "When?" : "last tuesday"},
    "contextoExample28" : {"What?" : "wind gust", "Where?" : "at sea near lanzarote", "When?" : "this week"},
    "contextoExample29" : {"What?" : "plankton", "Where?" : "coastal waters of taliarte", "When?" : "this year"},
    "contextoExample30" : {"What?" : "sailboats", "Where?" : "atlantic ocean", "When?" : "between the 10th and the 20th of the month"},
    "contextoExample31" : {"What?" : "average wave height", "Where?" : "the harbor", "When?" : "last friday"},
    "contextoExample32" : {"What?" : "boats", "Where?" : "the port", "When?" : "between 8 pm and midnight yesterday"},
    "contextoExample33" : {"What?" : "algae blooms", "Where?" : "fuerteventura", "When?" : "summer"},
    "contextoExample34" : {"What?" : "water temperature", "Where?" : "the harbor", "When?" : "2 pm"},
    "contextoExample35" : {"What?" : "fishing vessels", "Where?" : "", "When?" : "last 48 hours"},
    "contextoExample36" : {"What?" : "plankton", "Where?" : "gran canaria", "When?" : "right now"},
    "contextoExample37" : {"What?" : "weather", "Where?" : "the harbor", "When?" : "yesterday"},
    "contextoExample38" : {"What?" : "ships", "Where?" : "taliarte", "When?" : "last week"},
    "contextoExample39" : {"What?" : "air temperature", "Where?" : "the marina", "When?" : "sunday"},
    "contextoExample40" : {"What?" : "fishing boats", "Where?" : "fuerteventura", "When?" : "this month"},
    "contextoExample41" : {"What?" : "wind speed", "Where?" : "lanzarote", "When?" : "48 hours"},
    "contextoExample42" : {"What?" : "plankton", "Where?" : "gran canaria", "When?" : "last year"},
    "contextoExample43" : {"What?" : "water visibility", "Where?" : "las palmas", "When?" : "this morning"},
    "contextoExample44" : {"What?" : "algae blooms", "Where?" : "tenerife", "When?" : "month"},
    "contextoExample45" : {"What?" : "salinity level", "Where?" : "tenerife island", "When?" : "past week"},
    "contextoExample46" : {"What?" : "boats", "Where?" : "the bay", "When?" : ""},
    "contextoExample47" : {"What?" : "rainfall", "Where?" : "taliarte", "When?" : "past 3 days"},
    "contextoExample48" : {"What?" : "yachts", "Where?" : "coast of lanzarote", "When?" : "today"},
    "contextoExample49" : {"What?" : "average water temperature", "Where?" : "near the canary islands", "When?" : ""},
    "contextoExample50" : {"What?" : "phytoplankton", "Where?" : "tenerife", "When?" : "yesterday"},
    "contextoExample51" : {"What?" : "the current wind speed", "Where?" : "near the port of las palmas", "When?" : ""},
    "contextoExample52" : {"What?" : "motor boats", "Where?" : "taliarte", "When?" : "yesterday"},
    "contextoExample53" : {"What?" : "motor boats", "Where?" : "taliarte", "When?" : "last week"}
}
questions = {
    "1" : "What?",
    "2" : "Where?",
    "3" : "When?",
    "4" : "What time?"
}

def obtener_respuesta(pregunta, contexto):
    inputs = tokenizer.encode_plus(pregunta, contexto, return_tensors="pt", add_special_tokens=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
    start_logits, end_logits = outputs.start_logits, outputs.end_logits
    
    start_index = torch.argmax(start_logits)
    end_index = torch.argmax(end_logits) + 1
    
    respuesta_tokens = inputs["input_ids"][0][start_index:end_index]
    
    respuesta = tokenizer.decode(respuesta_tokens, skip_special_tokens=True)
    return respuesta
    
def testNerAccuracy():
    accuracies = {"What?": 0, "Where?": 0, "When?": 0, "What time?": 0}
    count = 0
    print("\n.....................Comenzando test.....................\n")
    for context in contextos.values():
        print(context + "\n")
        for question in questions.values():
            respuesta = obtener_respuesta(question, context)
            
            context_values_list = list(contextAnswers.values())
            specific_answer = context_values_list[count]
            for answers in specific_answer:
                final_answer = specific_answer[answers]
                if question == questions["1"]:
                    if final_answer == respuesta:
                        accuracies[question] += 1
                            
                if question == questions["2"]:
                    if final_answer == respuesta:
                        accuracies[question] += 1

                if question == questions["3"]:
                    if final_answer == respuesta:
                        accuracies[question] += 1
            print("Tu: " + question)
            print("BERT: " + respuesta)
        print("------------------------------------------------------------------------")
        count += 1
    print("\n......................Fin del test.......................\n")
    
    #print(accuracies)
    print("\n\n\n\n****************************|Resultados del test|****************************\n")
    print("El porcentaje de éxito del test ha sido:", round(accuracies["What?"]  / len(contextos) * 100, 3), "%, de aciertos para What?")
    print("El porcentaje de éxito del test ha sido:", round(accuracies["Where?"] / len(contextos) * 100, 3), "%, de aciertos para Where?")
    print("El porcentaje de éxito del test ha sido:",round(accuracies["When?"]   / len(contextos) * 100, 3), "%, de aciertos para When?\n")
    print("****************************|Resultados del test|****************************\n")



if __name__ == "__main__":
    testNerAccuracy()