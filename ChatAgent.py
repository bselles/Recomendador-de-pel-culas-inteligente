# -*- coding: utf-8 -*-
"""
Agente encargado de la interacción con el usuario
"""

from mesa import Agent
from intent_recognition import recognize_intent

class ChatAgent(Agent):
    '''
    userQuery = None
    
    intent = None
    entity = None
    
    askForEntity = {}
    
    noEntityQueries = {}
    
    askForQuery = "What can I help you with?\n"
    
    nothingRecognized = "Sorry I didn't understand what you mean" 
    '''
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
        self.userQuery = None
        self.intent = None
        self.entity = None
        self.askForEntity = {}
        self.noEntityQueries = {}
        self.askForQuery =  "What can I help you with?\n"
        self.nothingRecognized = "Sorry I didn't understand what you mean" 
        
        self.askForEntity["ask_for_recommendation_by_genre"] = "Sorry what genre were you asking about?"
        self.askForEntity["ask_for_recommendation_by_actor"] = "Sorry who did you mean? "
        self.askForEntity["ask_for_recommendation_by_director"] = "Sorry who did you mean? "
        self.askForEntity["ask_for_recommendation_by_runtime"] = "Sorry how long do you want the movie to last? "
        
        self.askForEntity["put_into_pending_list"] = "Sorry what film do you want to put in your pending list? "
        self.askForEntity["pop_from_pending_list"] = "Sorry what film do you want to remove from your pending list? "

        self.askForEntity["not_good_opinion"] = "Could you repeat the movie you didn't like please?"
        self.askForEntity["good_opinion"] = "Could you repeat the movie you enjoyed please?"
        
        self.askForEntity["ask_for_general_info"] = "What film is the one you wnat general information?"
        self.askForEntity["ask_for_plot"] = "Sorry what film's plot do you want to know?"
        self.askForEntity["ask_for_actors"] = "What is the film you are looking for it's cast?"
        self.askForEntity["ask_for_director"] = "Which film's director are you looking for?"
        self.askForEntity["ask_for_awards"] = "Which film is the one whose awards you want to know?"
        
        self.askForEntity["ask_for_score"] = "Sorry which film do you want to know it's general score?"
        self.askForEntity["ask_for_metacritic_score"] = "Could you repeat the film whose metacritic score you want to know?"
        self.askForEntity["ask_for_imdb_score"] = "I didn't understand the film whose imdb score you want to know"
        self.askForEntity["ask_for_rotten_score"] = "Sorry I couldn't understand the film whose Rotten Tomatoes score you want to know"
        
        self.noEntityQueries["ask_for_recommendation"] = None
        self.noEntityQueries["list_pending_list"] = None
        
    
    def step(self):
        #print("ChatAgent step")
        if self.model.pendingAnswer :
            # Hay una respuesta que devolver al usuario
            print(self.model.answer)    
            self.model.pendingAnswer = False
            return 
            
        if self.model.pendingQuery :
            # Todavia no se ha procesado la query anterior
            return 
        
        if self.intent == None : 
            # Realizamos una nueva query
            self.intent, self.entity = recognize_intent(input(self.askForQuery))
            
            if self.intent == "" :
                print(self.nothingRecognized)
                return 
                
            if self.entity != ""  or self.intent in self.noEntityQueries :
                #Tenemos una pregunta completa
                self.passQuery()
        
        else :
            # Nos faltó la entity por reconocer
            self.entity = recognize_intent(input(self.askForEntity[self.intent]))
            # Ahora sí tenemos una query completa
            self.model.passQuery()
            
        #self.userQuery = None
        
    def passQuery(self):
        self.model.entity = self.entity
        self.model.intent = self.intent
        self.model.pendingQuery = True
        
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