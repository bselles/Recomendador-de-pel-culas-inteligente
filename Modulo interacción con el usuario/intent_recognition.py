# -*- coding: utf-8 -*-

'''
    Módulo de reconocimiento de las intenciones del usuario.
'''

from rasa_nlu.model import Interpreter


def recognize_intent(user_input):
    interpreter = Interpreter.load("./models/current/nlu")
    result = interpreter.parse(user_input)
    print(result['intent']['name'])
    

recognize_intent( "What can you tell me about the godfather ")
recognize_intent( "Who are the actors of Gladiator ")
recognize_intent( "Who appears in Narnia ")
recognize_intent( "What can you tell me about the plot of Vinci ")
recognize_intent( "Who is in the cast of el padrino ")
recognize_intent( "What happens in cronicas de narnia ")
recognize_intent( "Can you resume her ")
recognize_intent( " What about the actors who appear in FILM")