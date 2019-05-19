# -*- coding: utf-8 -*-
"""
Modelo de control del sistema Multi-agente
"""

from ChatAgent import ChatAgent 
from DBAgent import DBAgent

from mesa import Model
from mesa.time import BaseScheduler
#from mesa.datacollection import DataCollector
#from mesa.space import ContinuousSpace

class Modelo (Model):
    
    ''' Modelo de los agentes '''
    '''
    intent = None
    entity = None
    pendingQuery = False
    
    answer = None
    pendingAnswer = False
    '''
    
    def __init__ (self):
        #print("iniciando scheduler")
        self.schedule = BaseScheduler(self)
        #print("iniciando DBAgent")
        self.schedule.add( DBAgent(0, self) )
        #print("iniciando chat")
        self.schedule.add( ChatAgent(1, self) )
        
        self.intent = None
        self.entity = None
        self.pendingQuery = False
        
        self.answer = None
        self.pendingAnswer = False
        
        #self.grid = ContinuousSpace
        #self.grid.place_agent(a, (0,0))
        #self.datacollector = DataCollector() 
        #model_reporters={"NombreDato": funcion() , }
        #agent_reporters={"NombreDato": atributo , }
        

    def step(self):
        #if self.answer != None :
        #    print(self.answer)
        #    self.answer = None 
        print("model step")
        self.schedule.step()    
        #self.datacollector.collect(self)
        
        
    def getDBAgent (self):
        return self.schedule.agents[0]
    
    def getChatAgent (self):
        return self.schedule.agents[1]

    
'''
if __name__ == "__main__" :
    model = Modelo( 3 )
    chat = ChatAgent( 1, Modelo )
    db = DBAgent(2, Modelo)
    chat.step()
    model.step()
    print("fin")
'''