# -*- coding: utf-8 -*-

'''
    Módulo de reconocimiento de las intenciones del usuario.
'''

from rasa_nlu.model import Interpreter

#Suprimimos los warnings.
import warnings
warnings.filterwarnings("ignore")

#Suprimimos los mensajes informativos de tensorflow.
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)



#Devuelve un par (intent, entity)
def recognize_intent(user_input):
    interpreter = Interpreter.load("./intent_recognition_model/models/current/nlu")
    result = interpreter.parse(user_input)
    #print("Entities")
    
    if (len(result['entities'])!=0):
        for x in result['entities']:
            entity=x["value"]
    else:
        entity=""
        return (result['intent']['name'], )
    
    return (result['intent']['name'],entity)
    
        
    #for x in result['entities']:
    #    print(str(x["value"]) + "---"+ str(x["entity"]))


'''
    TEST CASES
'''
test_cases= [\
     {"intent": "What can you tell me about The Godfather ", "solution":"ask_for_general_info"},\
     {"intent": "Who are the actors of Gladiator ", "solution": "ask_for_actors"},\
     {"intent": "Who appears in Narnia ", "solution":"ask_for_actors"},\
     {"intent":"What can you tell me about the plot of Vinci ", "solution":"ask_for_plot"},\
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

#print("DIFERENCIAS")
#print(test_system())