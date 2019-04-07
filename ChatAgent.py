# -*- coding: utf-8 -*-
"""
Agente encargado de la interacción con el usuario
"""

from mesa import Agent
from intent_recognition import recognize_intent

class ChatAgent(Agent):
	
	intent = None
	entity = None
	
	def __init__(self, unique_id, model):
		super().__init__(unique_id, model)
	
	def step(self):
		#print("ChatAgent step")
		if self.model.userQuery == None :
			# No hay nada que procesar
			#print("ChatAgent empty query")
			return 
		
		if self.intent == None : 
			# No tenemos ni intent ni entity
			self.intent, self.entity = recognize_intent(self.model.userQuery)
			self.model.userQuery = None
			if self.entity != "" :
				#Tenemos intent y entity 
				self.passQuery()

		else : 
			# ya hay intent pero no entity
			self.entity = self.model.userQuery
			self.model.userQuery = None
			self.passQuery()
		
	def passQuery(self):
		self.model.entity = self.entity
		self.model.intent = self.intent
		self.intent = None
		self.entity = None
	
	def parseQuery(self, query):
		"""
		parse = Parse(query)
		self.intent = parse.getIntent()
		self.entity = parse.getEntity()
		"""
		return True
	
#if __name__ == "__main__" :