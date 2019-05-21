# -*- coding: utf-8 -*-
"""
Agente encargado de la consulta de la base de datos y el aprendizaje
"""

from mesa import Agent
from Controller import Controller

class DBAgent(Agent):
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.control = Controller()
    
    def step(self):
        if self.model.pendingQuery :
            self.model.answer = self.control.procesa(self.model.intent, self.model.entity)
            self.model.pendingAnswer = True
            self.model.pendingQuery = False
