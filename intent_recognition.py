# -*- coding: utf-8 -*-

'''
   Módulo de reconocimiento de las intenciones del usuario.
   
   Dada una entrada introducida por el usuario, devuelve la intención (intent) asociada de entre
   todas las contempladas por el sistema. 
   
   Además, devuelve la entidad (si la encuentra) asociada a dicha intención.
'''

#Imports necesarios
from rasa_nlu.model import Interpreter
import warnings
import tensorflow as tf

#Para eliminar los warnings asociados.
warnings.filterwarnings("ignore") #Suprimimos los warnings.
tf.logging.set_verbosity(tf.logging.ERROR) #Suprimimos los mensajes informativos de tensorflow.


'''
    PARAMETROS DE CONFIGURACIÓN
'''

model_location="./intent_recognition_model/models/current/nlu"

'''
    FUNCIONALIDADES DEL MÓDULO
'''


'''
   1- RECONOCER UN INTENT:
        
        Dado un texto introducido por el usuario, busca entre todas las intenciones que detecta el sistema y devuelve 
        la asociada a dicho texto. Además, devuelve la entidad asociada a la intención (si la detecta.)
        
        Entrada:
            -user_input: cadena de caracteres que representa el texto introducido por el usuario.
            
        Salida:
            -Un par donde:
                En la primera posición se devolverá el texto que representa el intent detectado.
                En la segunda posición una cadena de caracteres que representa la entidad asociada al intent detectado. Si no se detecta ninguna entidad, devolverá "".
'''
def recognize_intent(user_input):
    interpreter = Interpreter.load(model_location)
    result = interpreter.parse(user_input)
    
    if (len(result['entities'])!=0):
        for x in result['entities']:
            entity=x["value"]
    else:
        entity=""
    
    return (result['intent']['name'],entity)

'''
    CASOS DE PRUEBA
'''

if __name__ == "__main__":
    test_cases= [\
         {"intent": "I don't like films like Avatar ", "solution":"not_good_opinion"},\
         {"intent": "I love Gladiator ", "solution": "good_opinion"},\
         {"intent": "Recommend me a film please", "solution":"ask_for_recommendation"},\
         {"intent":"Tell me a film to watch", "solution":"ask_for_recommendation"},\
         {"intent": "Next time don't recommend me films like Avatar", "solution":"not_good_opinion"},\
         {"intent": "Next time recommend me films like Avatar", "solution": "good_opinion"},\
         {"intent": "I've seen Her and i liked it", "solution":"good_opinion"},\
         {"intent":"I've seen Her and I didn't like it", "solution":"not_good_opinion"},\
         
         {"intent":"Who is in the cast of el padrino ", "solution":"ask_for_actors"},\
         {"intent":"What happens in Narnia Chronicles ", "solution":"ask_for_plot"},\
         {"intent":" What about the actors who appear in Film", "solution":"ask_for_actors"},\
         {"intent": "What do the people from metacritic think about Her?", "solution":"ask_for_metacritic_score"},\
         {"intent":"What do the people think about Her?", "solution":"ask_for_score"},\
         {"intent": "Can you punctuate Avatar?", "solution":"ask_for_score"},\
         {"intent":"Does Avatar have any award?", "solution":"ask_for_awards"},\
         {"intent": "Which is the punctuation of Her?", "solution":"ask_for_score"},\
         {"intent": "Which is the punctuation of her in rotten tomatoes?", "solution":"ask_for_rotten_score"},\
         {"intent":"Which is the punctuation of Her in rotten?", "solution":"ask_for_rotten_score"},\
         {"intent": "What do they think in metacritic about Lost?", "solution":"ask_for_metacritic_score"},\
         {"intent":"What do they think in imdb about Green Day?", "solution":"ask_for_imdb_score"},\
         {"intent":"Which is the punctuation of Lost?", "solution":"ask_for_score"},\
         {"intent":"Tell me the punctuation of Lost?", "solution":"ask_for_score"},\
         {"intent":"What could you tell me about Lost?", "solution":"ask_for_general_info"},\
         {"intent":"What could you tell me about it?", "solution":"ask_for_general_info"},\
         {"intent":"Which is his score?", "solution":"ask_for_score"},\
         {"intent":"Tell me the plot?", "solution":"ask_for_plot"},\
         {"intent":"Who appears in this movie?", "solution":"ask_for_actors"},\
         {"intent":"What can you tell me about the film?", "solution":"ask_for_general_info"},\
         ]
    
    
    def test_system():
        correct=0    
        for x in test_cases:
            print("---------")
            print(x["intent"])
            result=recognize_intent(x["intent"])
            if(result[0]!=x["solution"]):
                print(x["intent"])
                print(result[0])
                print(x["solution"])
                print("---------")
            else:
                correct=correct+1
        return (correct*100)/len(test_cases)
    
    print(test_system())
