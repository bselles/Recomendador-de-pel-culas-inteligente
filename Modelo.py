# -*- coding: utf-8 -*-
"""
Modelo de control del sistema Multi-agente
"""

from ChatAgent import ChatAgent 
from DBAgent import DBAgent

from mesa import Model
from mesa.time import BaseScheduler

class Modelo (Model):
    
    def __init__ (self):
        self.schedule = BaseScheduler(self)
        self.schedule.add( DBAgent(0, self) )
        self.schedule.add( ChatAgent(1, self) )
        
        self.intent = None
        self.entity = None
        self.pendingQuery = False
        
        self.answer = None
        self.pendingAnswer = False
        

    def step(self):
        self.schedule.step()    
