# -*- coding: utf-8 -*-
"""
Agente encargado de la consulta de la base de datos y el aprendizaje
"""

from mesa import Agent
from Controller import Controller

class DBAgent(Agent):
    #control = Controller()
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        print("iniciando controller")
        self.control = Controller()
    
    def step(self):
        #print("DBAgent step")
        if self.model.pendingQuery :
            print("El intent es " + self.model.intent + " y la entity " + self.model.entity)
            self.model.answer = self.control.procesa(self.model.intent, self.model.entity)
            self.model.pendingAnswer = True
            self.model.pendingQuery = False
            
    

#if __name__ == "__main__" :