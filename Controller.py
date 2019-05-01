# -*- coding: utf-8 -*-

'''
    Módulo controlador.
'''

#Imports necesarios para el funcionamiento del sistema
from intent_recognition import recognize_intent
from omdb_module import get_movie_info , search_for_movie ,get_rottentomatoes_score
from trained_model import Trained_Model
from pathlib import Path
import random


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
        self.pr_size=50
        
        #fichero que almacena las posibles peliculas a recomendar.
        self.pr_filename='prfn'
        
        #diccionario que almacenará las potenciales recomendaciones (títulos de películas)
        self.pot_rec= self.__init_potential_recom()
        
        #Modelo que se entrenará para que el sistema infiera buenas recomendaciones.
        self.tm = Trained_Model() 
        
    
    '''
        Carga self.pr_size títulos de películas en self.pot_rec. Estas serán las que se utilizarán para recomendar al usuario.    
    '''
    def __init_potential_recom(self):
        
        result={}
        
        #Leemos todas las películas.
        with open(self.pr_filename, "r") as f:
            lines = f.readlines()
                
        #Insertamos las pr_size primeras películas en el diccionario.
        for x in range(self.pr_size):
            result[x]=lines[x].strip('\n')
        
        #Eliminamos las películas del fichero. Para ello, escribimos las siguientes (obviando las self.pr_size primeras)        
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

    '''
        Dada una intención detectada y la entidad asociada (si existe), llama al módulo correspondiente (a la funcionalidad asociada)
        para responder a la solicitud del usuario.
    '''

    def procesa(self,intent, entity):
        
        #Si el intent no tiene que ver con obtener información sobre una película.
        if(intent=="ask_for_recommendation"):
            return self.__get_recommended_film()        
        
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
            return self.__parse_score_info(score,'Metacritic')
            
        elif(intent=="ask_for_imdb_score"):
            score=float(info['imdbRating'])
            return self.__parse_score_info(score,'IMDB')
            
        elif(intent=="ask_for_rotten_score"):            
            score=float( get_rottentomatoes_score(info))
            return self.__parse_score_info(score,'rotten tomatoes')
            
        elif(intent=="ask_for_score"):
            result= "Well, I don't know what people think about this film but I can tell you which scores do this movie have in different sites.\n"
            
            result= result+ "Rottentomatoes score: " + get_rottentomatoes_score(info) + "\n"
            result= result+ "IMDB score: " + info['imdbRating'] + "\n"
            result= result+ "Metacritic score: " + info['Metascore'] + "\n"

        
        
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
                            #Añadimos la película como recomendada en el diccionario.
                            self.recommended_movies[title]=None
                            #Añadimos la película como recomendada en el fichero.
                            self.__write_on_file(self.recommended_filename,title)

                            return title
                        
                except Exception as e:
                    print(index)
                    #Si hubo algún problema, sustituimos la película actual por una nueva.
                    self.pot_rec[index]=self.__get_first_and_delete()                  
                    print(e)
                    print('Error con la película '+ str(film))
            
        return "" #Implica error.        
        
    
    '''
        Dado un JSON con la información asociada a una pelícla, la devuelve con un formato legible para el usuario.
    '''
    def __parse_general_info(self,info):   
        
        result=''
        result=result+"Well, let's see what I find about "+info['Title'] +'\n'
        result=result+"It's release date was: "+ info['Released']+'\n'
        result=result+"Some people from the cast: " + info['Actors']+'\n'
        
        result=result+"And the director is "+info['Director']+' \n'
        result=result+"Summary of the plot: \n" + info['Plot'] + "\n"
        result=result+"IMDB score:" +'\n' 
        result=result+ self.__parse_score_info(float(info['imdbRating']),'IMDB')+ '\n'
        
        result=result+"Rotten Tomatoes score:" +'\n'
        result=result+ self.__parse_score_info(float( get_rottentomatoes_score(info)),'Rotten tomatoes')+ '\n'
        result=result+"Metacritic score:" +'\n'
        result=result+ self.__parse_score_info(float( info['Metascore']),'Metacritic')+ '\n'
       
        return result



    '''
        Dado el nombre de un fichero y el titulo de una película, escribe al final del fichero dicho título.
    '''
    def __write_on_file(self,filename, film):        
         with open(filename, "a") as myfile:
                myfile.write(film+'\n')
            
    
    '''
        Elimina la primera línea de un fichero. 
    '''
    def __get_first_and_delete(self):
        with open(self.pr_filename, "r") as f:
            lines = f.readlines() 
                
        result=lines[0].strip('\n')
        
        with open(self.pr_filename, "w") as f:
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
    

    
    
