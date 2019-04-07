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
	
	userQuery = None
	
	intent = None
	entity = None
	
	answer = None
	
	
	def __init__ (self):
		self.schedule = BaseScheduler(self)
		self.schedule.add( DBAgent(0, self) )
		self.schedule.add( ChatAgent(1, self) )
		#self.grid = ContinuousSpace
		#self.grid.place_agent(a, (0,0))
		#self.datacollector = DataCollector() 
		#model_reporters={"NombreDato": funcion() , }
		#agent_reporters={"NombreDato": atributo , }
		

	
	def step(self):
		self.schedule.step()	
		#self.datacollector.collect(self)
		
		
	def getDBAgent (self):
		return self.schedule.agents[0]
	
	def getChatAgent (self):
		return self.schedule.agents[1]
	
	def queryReady():
		return True
	
'''
if __name__ == "__main__" :
	model = Modelo( 3 )
	chat = ChatAgent( 1, Modelo )
	db = DBAgent(2, Modelo)
	chat.step()
	model.step()
	print("fin")
'''