# -*- coding: utf-8 -*-
"""
Script de prueba del sistema con Agentes
La idea es combinar esto con el Controller y formar el "launcher" del sistema
"""

from Modelo import Modelo
#from ChatAgent import ChatAgent 
#from DBAgent import DBAgent


if __name__ == "__main__" :
    model = Modelo()
    while True:
        model.step()
