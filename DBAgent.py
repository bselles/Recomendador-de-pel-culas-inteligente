# -*- coding: utf-8 -*-
"""
Agente encargado de la consulta de la base de datos y el aprendizaje
"""

from mesa import Agent
from Controller import procesa

class DBAgent(Agent):
	
	result = "ResultadoVacio"
	
	def __init__(self, unique_id, model):
		super().__init__(unique_id, model)
	
	def step(self):
		#print("DBAgent step")
		if self.model.entity != None :
			self.model.answer = procesa(self.model.intent, self.model.entity)
			self.model.entity = None
			self.model.intent = None
			
	

#if __name__ == "__main__" :