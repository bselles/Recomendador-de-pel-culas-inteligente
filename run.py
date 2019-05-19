# -*- coding: utf-8 -*-
"""
Script de prueba del sistema con Agentes
La idea es combinar esto con el Controller y formar el "launcher" del sistema
"""

from Modelo import Modelo
#from ChatAgent import ChatAgent 
#from DBAgent import DBAgent


if __name__ == "__main__" :
    #print("iniciando run.py")
    model = Modelo()
    #model.userQuery = "What can you tell me about Avtar?"
    print("modelo creado")
    while True:
        #print("ejecución bucle")
        model.step()
    '''
    while True:
        model.userQuery = input('What can I help you with?')
        model.step()
        if model.entity == None and model.intent!="ask_for_recommendation" :
            model.userQuery = input('Which film are you talking about? \n')
        model.step()
        model.step()
        model.step()
        model.step()
        print(model.answer)
        #print("El modelo ha acabado con") 
        #print(model.entity)
        #print(model.intent)
        #print("fin")
    '''
    pass