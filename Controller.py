# -*- coding: utf-8 -*-

'''
    Módulo controlador.
'''


from intent_recognition import recognize_intent
from omdb_module import get_movie_info , search_for_movie ,get_rottentomatoes_score#, get_summary_plot, get_actors,get_director, get_awards,get_metacritic_score, get_imdb_score, get_rottentomatoes_score
from trained_model import Trained_Model
from pathlib import Path
import random

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
        
        
        #potential recomendations size. Numero de películas que aspirarán a ser recomendadas en cada selección aleatoria. El parámetro es configurable.
        self.pr_size=500
        self.pr_filename='prfn'
        
        self.pot_rec= self.__init_potential_recom()
        
        #Modelo que se entrenará para que el sistema infiera buenas recomendaciones.
        self.tm = Trained_Model() 
        
        
    def __init_potential_recom(self):
        
        result={}
        
        #Leemos todas las películas.
        with open(self.pr_filename, "r") as f:
            lines = f.readlines()
                
        #Insertamos las pr_size primeras películas en el diccionario.
        for x in range(self.pr_size):
            result[x]=lines[x].strip('\n')
        
        #Eliminamos las películas del fichero.
        #with open(self.pr_filename, "r") as f:
        #    lines = f.readlines()
        
        with open(self.pr_filename, "w") as f:
            for x in range(self.pr_size-1,len(lines)):
                f.write(lines[x])

        return result

    '''
        Dado el nombre de un fichero que contiene nombres de películas, devuelve un diccionario cuyas claves serán esos nombres y su valor será NULL.
        
        Se utiliza para inicializar recommended_films y not_to_recommend_films
    '''
    def __init_names_dict(self, filename):
        
        if not Path(filename).is_file():
            #creamos el fichero si no existe
            with open(filename, "w+") as myfile:
               #No sucederá nada. Solo se creará el fichero.
               print(filename+' created')
            
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
        
        #Si el intent no tiene que ver con obtener información sobre una película.
        
        if(intent=="ask_for_recommendation"):
            
            while True:
                #Generamos un número aleatorio.
                index=random.randint(0,self.pr_size-1)
                
                #Obtenemos la película asociada a esa posición aleatoria.
                film=self.pot_rec[index]
                
                #Nos aseguramos de que la película sea válida.
                try:
                    #Buscamos el título que tiene asociado en IMDB
                    title=search_for_movie(film)
                    
                    if (title == ""):
                        self.pot_rec[index]=self.__get_first_and_delete()                  
                    if ('YES'== self.tm.get_recommendation(title)):
                        self.pot_rec[index]=self.__get_first_and_delete()                  
                        if not(title in self.not_to_recommend.keys()) and not (title in self.recommended_movies.keys()):
                            #Añadimos la película como recomendada.
                            self.recommended_movies[title]=None
                            return title
                        
                except Exception as e:
                    print(index)
                    #Si hubo algún problema, sustituimos la película actual por una nueva.
                    self.pot_rec[index]=self.__get_first_and_delete()                  
                    print(e)
                    print('Error con la película '+ str(film))
                
            
            return "" #Implica error.        
        
        #Obtenemos la película a la que se refería el usuario con la entrada.
        title=search_for_movie(entity)
        
        if title == "":
            #No se ha encontrado ningún resultado para esa película.
            return "Sorry, I don't know which film you're talking about."
        
        if(intent=="not_good_opinion"):
            
            #Almacenamos que esa película no le gusta para no recomendarsela en un futuro.
            self.not_to_recommend[title]=None
            self.__write_on_file(self.not_to_rec_filename,title)
            
            self.tm.add_opinion(entity,'NO')
            return "It seems you don't like "+ title+".I'll remember it"
        elif(intent=="good_opinion"):
            self.tm.add_opinion(entity,'YES')
            return "Did you like it? Perfect. I'll remember it :)"

        
        #Si el intent tiene que ver con obtener información sobre una película.
        
        #Obtenemos la información de la película introducida por el usuario.
        info=get_movie_info(title)
        
        if(intent=="ask_for_general_info"):
            return self.__parse_general_info(info)
        elif(intent=="ask_for_plot"):
            return 'Here you go a summary of the plot of '+ title +':\n'+ info['Plot']
        elif(intent=="ask_for_actors"):
            return 'The main stars that appear in ' +  title + ' are '+ info['Actors']
        elif(intent=="ask_for_director"):
            return 'The director of '+ title + ' is '+ info['Director']
        elif(intent=="ask_for_awards"):
            return 'These are the awards that '+ title +' won:\n' + info['Awards']
        elif(intent=="ask_for_metacritic_score"):            
            score=float(info['Metascore'])
            
            if(score>8):
                return 'It seems that the people from Metacritic enjoyed this film. It have a '+ str(score)
            elif(score>6):
                return 'It has a '+ str(score)+". Seems that they kind of like it but its not the best film they've seen."
            else:
                return "They don't seem to like it a lot. It has a "+ str(score) 
            
        elif(intent=="ask_for_imdb_score"):
            
            score=float(info['imdbRating'])
            
            if(score>8):
                return 'It seems that the people from IMDB enjoyed this film. It have a '+ str(score)
            elif(score>6):
                return 'It has a '+ str(score)+". Seems that they kind of like it but its not the best film they've seen."
            else:
                return "They don't seem to like it a lot. It has a "+ str(score)

        elif(intent=="ask_for_rotten_score"):
            
            score=float( get_rottentomatoes_score(info))
            
            if(score>8):
                return 'It seems that the people from IMDB enjoyed this film. It have a '+ str(score)
            elif(score>6):
                return 'It has a '+ str(score)+". Seems that they kind of like it but its not the best film they've seen."
            else:
                return "They don't seem to like it a lot. It has a "+ str(score) 
            
        elif(intent=="ask_for_score"):
            result= "Well, I don't know what people think about this film but I can tell you which scores do this movie have in different sites.\n"
            
            result= result+ "Rottentomatoes score: " + get_rottentomatoes_score(info) + "\n"
            result= result+ "IMDB score: " + info['imdbRating'] + "\n"
            result= result+ "Metacritic score: " + info['Metascore'] + "\n"

        
        
            return result
        else:
            return "I don't understand what you're asking for. Can you repeat it in a different way?"
    
    
    
    def __parse_general_info(self,info):        
        return info
    
    def __write_on_file(self,filename, film):        
         with open(filename, "a") as myfile:
                myfile.write(film+'\n')
            
    
    def __get_first_and_delete(self):
        with open(self.pr_filename, "r") as f:
            lines = f.readlines() 
                
        result=lines[0].strip('\n')
        
        with open("file.txt", "w") as f:
            count = range(1,len(lines))
            for i in  count:
                f.write(lines[i])
                
        return result
        
        

if __name__ == "__main__" :

    c=Controller()
    
    
    while True:
        example= input('Insert here: \n')
    
        intent, entity= recognize_intent(example)
    
        print(intent)
        print(entity)
        if(entity=="" and intent!="ask_for_recommendation"):
            entity=input("Which film are you talking about?  \n")
        
        print(c.procesa(intent, entity))
    

    
    
