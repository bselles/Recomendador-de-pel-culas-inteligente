# -*- coding: utf-8 -*-

'''
    Módulo controlador.
'''

#Imports necesarios para el funcionamiento del sistema
from intent_recognition import recognize_intent
from trained_model import Trained_Model
from pathlib import Path
import random
from pymongo import MongoClient


'''
    ACCESO A LA BD MONGO
'''
        
client = MongoClient('mongodb://127.0.0.1:27017')
db = client.recomendadorpeliculas 

'''
    Clase que interacuará con los demás elementos del sistema para implementar el comportamiento
    del propio sistema.
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
                
        self.not_to_rec_filename='ntrmdb'
        self.not_to_recommend=self.__init_names_dict(self.not_to_rec_filename)         #Películas que ha dicho de forma explícita que no le gustan.
        
        #potential recomendations size. Numero de películas que aspirarán a ser recomendadas en cada selección aleatoria. El parámetro es configurable.
        self.pr_size=468

        #Modelo que se entrenará para que el sistema infiera buenas recomendaciones.
        self.tm = Trained_Model() 
        
        #Diccionario que almacena la lista de pendientes.
        self.pending_list_file= 'pldb'
        self.pending_list=self.__init_names_dict(self.pending_list_file)
        
        #Diccionario que almacena los nombres de las películas que maneja el sistema.
        self.film_names_file= 'films_names'
        self.film_names=self.__init_names_dict(self.film_names_file)
    
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

    '''
        Dada una intención detectada y la entidad asociada (si existe), llama al módulo correspondiente (a la funcionalidad asociada)
        para responder a la solicitud del usuario.
    '''

    def procesa(self, intent, entity):
        
        #Si el intent no tiene que ver con obtener información sobre una película.
        if(intent=="ask_for_recommendation"):
            return self.__get_recommended_film()        
        elif(intent=="list_pending_list"):
            return self.__parse_pending_list()
    
    
        if(intent=="ask_for_recommendation_by_genre"):
            return self.__get_recommended_parameter("genre",entity)
        elif(intent=="ask_for_recommendation_by_actor"):
            return self.__get_recommended_parameter("actor",entity)
        elif(intent=="ask_for_recommendation_by_director"):
            return self.__get_recommended_parameter("director",entity)
        elif(intent=="ask_for_recommendation_by_runtime"):
            return self.__get_recommended_parameter("runtime",entity)
            
        #Obtenemos la película a la que se refería el usuario con la entrada.
        if not entity in self.film_names.keys():
            #No se ha encontrado ningún resultado para esa película.
            return "Sorry, I don't know which film you're talking about."
        
        title=entity
        
        if(intent=="put_into_pending_list"):
            if title in self.pending_list:
                return title +  ' is already in your pending list'
            
            self.pending_list[title]=None
            self.__change_list_pending_file()

            return title+ " it's now in your pending list"
            
        elif(intent=="pop_from_pending_list"):
            if not title in self.pending_list:
                return title+ ' is not in your pending list'
            del self.pending_list[title]
            self.__change_list_pending_file()

            return title + ' popped from the pending list'

            
        
        if(intent=="not_good_opinion"):
            #Almacenamos que esa película no le gusta para no recomendarsela en un futuro.
            self.not_to_recommend[title]=None
            self.__write_on_file(self.not_to_rec_filename,title)
            self.tm.add_opinion(entity,'NO')
            
            #Si está dentro de la pending list, la quitamos.
            if title in self.pending_list:
                del self.pending_list[title]
            self.__change_list_pending_file()
            
            return "It seems you don't like "+ title+".I'll remember it"
        
        elif(intent=="good_opinion"):
            self.tm.add_opinion(entity,'YES')
            
            #Si está dentro de la pending list, la quitamos.
            if title in self.pending_list:
                del self.pending_list[title]
                
            self.__change_list_pending_file()
            
            return "Did you like it? Perfect. I'll remember it :)"

        
        #Si el intent tiene que ver con obtener información sobre una película.
        #Obtenemos la información de la película introducida por el usuario.       
        info=self.__get_info_from_db(title)
        
        
        if(intent=="ask_for_general_info"):
            return self.__parse_general_info(info)
        
        elif(intent=="ask_for_plot"):
            return 'Here you go a summary of the plot of '+ title +':\n'+ info['Plot']
        
        elif(intent=="ask_for_actors"):
            return 'The main stars that appear in ' +  title + ' are '+ ', '.join(info['Actors'])
        
        elif(intent=="ask_for_director"):
            return 'The director of '+ title + ' is '+ info['Director']
        
        elif(intent=="ask_for_awards"):
            return 'These are the awards that '+ title +' won:\n' + str(info['Awards'])
        
        elif(intent=="ask_for_metacritic_score"):            
            score=float(info['Metacritic'])/10
            return self.__parse_score_info(score,'Metacritic')
            
        elif(intent=="ask_for_imdb_score"):
            score=float(info['Internet Movie Database'])
            return self.__parse_score_info(score,'IMDB')
            
        elif(intent=="ask_for_rotten_score"):            
            score=float(info['Rotten Tomatoes'])
            return self.__parse_score_info(score/10,'rotten tomatoes')
            
        elif(intent=="ask_for_score"):
            result= "Well, I don't know what people think about this film but I can tell you which scores do this movie have in different sites.\n"
            result= result+ "Rottentomatoes score: " + str(info['Rotten Tomatoes']/10) + "\n"
            result= result+ "IMDB score: " + str(info['Internet Movie Database']) + "\n"
            result= result+ "Metacritic score: " + str(info['Metacritic']/10) + "\n"
            return result
        else:
            return "I don't understand what you're asking for. Can you repeat it in a different way?"
    
    '''
        Dada una nota (double)  y el sitio en el cual se ha obtenido, devuelve una frase adaptada a la nota y el sitio.
        Esta frase será la que se devuelva al usuario cuando este solicite esta información.
    ''' 
    def __parse_score_info(self,score, site):
            
        if(score>8):
            return 'It seems that the people from '+ site +' enjoyed this film. It have a '+ str(score)
        elif(score>6):
            return 'It has a '+ str(score)+". Seems that they kind of like it but its not the best film they've seen."
        else:
            return "They don't seem to like it a lot. It has a "+ str(score) 
    
    '''
        Devuelve una cadena de caracteres que incluirá todas las películas que contiene la lista de pendientes.
    
    '''
    def __parse_pending_list(self):
        result="This is your pending list: \n"
        for x, y in self.pending_list.items():
            result= result+ x + '\n'
            
        return result
    
    '''
        En función de los gustos del usuario inferidos por el sistema, el sistema realiza una recomendación. La recomendación consistirá en 
        un título de una película.
        En el caso de que no encuentre ninguna película para recomendarle al usuario, devuelve "".
        
        Input:
            -nada
        Ouput:
            Cadena de caracteres que:
                -es el título de una película si no sucedió ningún error.
                -'' en el caso de que suceda algún error.
    '''
    def __get_recommended_film(self):
        while True:
                #Generamos un número aleatorio.
                index=random.randint(1,self.pr_size)
                #Obtenemos la película asociada a esa posición aleatoria.
                film=self.__get_film_info_db_id(index)
                if film!="":
                    #Nos aseguramos de que la película sea válida.
                    try:
                        #Buscamos el título que tiene asociado en IMDB
                        title=film['Title']

                        if(title!="" and self.tm.get_recommendation(title)=='YES'):
                             if(not title in self.not_to_recommend.keys() and not(title in self.recommended_movies.keys())):
                                #Añadimos la película como recomendada en el diccionario.
                                self.recommended_movies[title]=None
                                #Añadimos la película como recomendada en el fichero.
                                self.__write_on_file(self.recommended_filename,title)
                                return title
                    except :
                        print('')

            
        return "" #Implica error.        
    
    '''
        Devuelve un listado de películas en las que se cumple que el valor del parámetro "parameter" es entity.
        
        Es decir, si parameter es "actor", devuelve películas en las que aparezca ese actor o si parameter es "genre" devuelve
        películas de ese género.
    '''
    def __get_recommended_parameter(self,parameter,entity):
        
        if parameter=='actor':
            films=self.__get_films_by_actor(entity)
        elif parameter=='director':
            films=self.__get_films_by_director(entity)
        elif parameter=='runtime':
            films=self.__get_films_by_Runtime(entity)
        elif parameter=='genre':
            films=self.__get_films_by_genre(entity)
            
        for x in films:

            title=x['Title']
            if(self.tm.get_recommendation(title)=='YES' and (not title in self.not_to_recommend.keys()) and (not title in self.recommended_movies.keys())):
                self.recommended_movies[title]=None
                self.__write_on_file(self.recommended_filename,title)
                return title
        return "" #Implica error.
    
    
    '''
        Dado el id de una película, la busca en la BD Mongo y devuelve la información asociada.
    '''
    def __get_film_info_db_id(self,ID):
        
        myquery = { "id": ID }
        mydoc = list(db.peliculas.find(myquery))
        
        if(len(mydoc)==0):
            return ""
        
        return mydoc[0]
    
    '''
        Dado un JSON con la información asociada a una pelícla, la devuelve con un formato legible para el usuario.
    '''
    def __parse_general_info(self,info):   
        
        result=''
        result=result+"Well, let's see what I find about "+info['Title'] +'\n'
        result=result+"It's release date was: "+ info['Released']+'\n'
        result=result+"Some people from the cast: " + ', '.join(info['Actors'])+'\n'
        
        result=result+"And the director is "+info['Director']+' \n'
        result=result+"Summary of the plot: \n" + info['Plot'] + "\n"
        result=result+"IMDB score:" +'\n' 
        result=result+ self.__parse_score_info(float(info['Internet Movie Database']),'IMDB')+ '\n'
        
        result=result+"Rotten Tomatoes score:" +'\n'
        result=result+ self.__parse_score_info(float(info['Rotten Tomatoes']/10),'Rotten tomatoes')+ '\n'

        result=result+"Metacritic score:" +'\n'
        result=result+ self.__parse_score_info(float( info['Metacritic']/10),'Metacritic')+ '\n'
       
        return result


    
    '''
        Dado el nombre de un fichero y el titulo de una película, escribe al final del fichero dicho título.
    '''
    def __write_on_file(self,filename, film):        
         with open(filename, "a") as myfile:
                myfile.write(film+'\n')
            
    '''
        En función del contenido de la lista de películas pendientes, modifica el contenido del fichero que almacena las listas pendientes. 
    '''
    def __change_list_pending_file(self):
        with open(self.pending_list_file, "w") as myfile:
            for x, y in self.pending_list.items():
                myfile.write(x+'\n')
    
    def __get_info_from_db(self,name):        
        return list(db.peliculas.find({ "Title": name }))[0]
        
    def __get_films_by_genre(self,genre):
        return list(db.peliculas.find({ "Genre": genre }))
    
    def __get_films_by_director(self,director):
        return list(db.peliculas.find({ "Director": director }))
    
    def __get_films_by_actor(self,actor):
        return list(db.peliculas.find({ "Actors": actor }))
    
    def __get_films_by_Runtime(self, runtime):
        if runtime=="short":
            query= { "Runtime": { '$lt': 90 } }
        elif runtime=="medium":
            query={ '$and': [ { "Runtime": { '$lt': 120 } }, { "Runtime": { '$gt': 90 } }  ]  } 
        elif runtime=="large":
            query= { "Runtime": { '$gt': 120 } }

        return list(db.peliculas.find( query ))


if __name__ == "__main__" :

    c=Controller()
    
    
    while True:
        example= input('What can I do for you? \n')
    
        intent, entity= recognize_intent(example)

        if(entity=="" and intent!="list_pending_list" and intent!="ask_for_recommendation" ):
            entity=input("Which film are you talking about?  \n")
        print('\n')
        print(c.procesa(intent, entity))
    

    
    
