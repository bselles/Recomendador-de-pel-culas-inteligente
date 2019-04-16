# -*- coding: utf-8 -*-

'''
    Módulo controlador.
'''


from intent_recognition import recognize_intent
from omdb_module import get_movie_info, get_summary_plot, get_actors,get_director, get_awards,get_metacritic_score, get_imdb_score, get_rottentomatoes_score
from trained_model import Trained_Model
from pathlib import Path



#Variables globales

'''
tm=Trained_Model()


ftr=['Avatar','Looper','Her','War', 'Warcraft', 'Dunkirk', 'The Prestige']

recommended_movies={} #Películas que ya han sido recomendadas.
not_to_recomend={}
'''

class Controller:
    
    def __init__(self):
        
        #Se usan diccionarios para disminuir la complejidad.
        
        #Películas que contemplará el sistema para recomendar.
        self.bbdd_dict={}
        
        #Potenciales películas para recomendar en una cierta recomendación.
        self.tmp_movies={}
        
        #Información asociada a las consultas previas del usuario.
        self.recommended_filename='rmdb'
        self.recommended_movies=self.__init_names_dict(self.recommended_filename)      #Películas que le han recomendado previamente.
        
        print(self.recommended_movies)
        
        self.not_to_rec_filename='ntrmdb'
        self.not_to_recommend=self.__init_names_dict(self.not_to_rec_filename)         #Películas que ha dicho de forma explícita que no le gustan.
        
        print(self.not_to_recommend)
        
        #Modelo que se entrenará para que el sistema infiera buenas recomendaciones.
        self.tm = Trained_Model() 

    '''
        Dado el nombre de un fichero que contiene nombres de películas, devuelve un diccionario cuyas claves serán esos nombres y su valor será NULL.
        
        Se utiliza para inicializar recommended_films y not_to_recommend_films
    '''
    def __init_names_dict(self, filename):
        
        if not Path(filename).is_file():
            #creamos el fichero si no existe
            with open(filename, "w+") as myfile:
               myfile.write("\n")
            
            #Devolvemos un diccionario vacío porque el fichero no contenía ninguna película.
            return {}
        else:
            #Si el fichero existe, leemos su contenido y lo insertamos en el diccionario. 
            
            result={}
            with open(filename, "r") as myfile:
               content=myfile.readlines()
            
            for x in content:
                result[x.replace('\n',"")]=None            
        
        return result


   

    def procesa(self,intent, entity):
        if(intent=="ask_for_general_info"):
            return get_movie_info(entity)
        elif(intent=="ask_for_plot"):
            return get_summary_plot(entity)
        elif(intent=="ask_for_actors"):
            return get_actors(entity)
        elif(intent=="ask_for_director"):
            return get_director(entity)
        elif(intent=="ask_for_awards"):
            return get_awards(entity)
        elif(intent=="ask_for_metacritic_score"):
            return get_metacritic_score(entity)
        elif(intent=="ask_for_imdb_score"):
            return get_imdb_score(entity)
        elif(intent=="ask_for_rotten_score"):
            return get_rottentomatoes_score(entity)
        elif(intent=="not_good_opinion"):
            self.not_to_recomend[entity]=True
            self.tm.add_opinion(entity,'NO')
            return "Thanks for giving your opinon"
        elif(intent=="good_opinion"):
            self.tm.add_opinion(entity,'YES')
            return "Thanks for giving your opinon"
        elif(intent=="ask_for_recommendation"):
            '''
            i=0
            resul = ""
            while(i<len(self.ftr)  ):
                if('YES'== self.tm.get_recommendation(self.[i]) and not (self.ftr[i] in recommended_movies) and not(ftr[i] in not_to_recomend) ):
                    recommended_movies[ftr[i]]=True
                    resul = resul + ftr[i] + "\n"
                    i=len(ftr)
                i=i+1
            return resul
            '''
        elif(intent=="ask_for_score"):
            #return get_movie_info(entity))
            return "MOSTRARIA NOTAS"
        else:
            return "El intent no se ha encontrado correctamente"
    
    
    
    


if __name__ == "__main__" :

    c=Controller()
    
    '''
    while True:
        example= input('Insert here: \n')
    
        intent, entity= recognize_intent(example)
    
        print(intent)
        if(entity=="" and intent!="ask_for_recommendation"):
            entity=input("Which film are you talking about?  \n")
        
        #print(procesa(intent, entity))
    '''

    
    
