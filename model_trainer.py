# -*- coding: utf-8 -*-


'''
    Dado una película y si se recomendaría o no, se genera el nuevo dataset.
'''


#Imports necesarios
from omdb_module import get_movie_info
from pathlib import Path


'''
    PARÁMETROS DE CONFIGUTACIÓN DEL MÓDULO
'''

parameters=['director','Runtime','Genre','Subgenre','metacritic','imdb','rotten']   #Nombre de las columnas (en orden) del fichero de entrenamiento/test que se van a utilizar en la tarea.
training_data= "file.train"                                                         #Localización/nombre del fichero con los ejemplos de entrenamiento.
test_data="file.test"                                                               #Localización/nombre del fichero con los ejemplos de testing del modelo.


'''
    FUNCIONALIDADES ASOCIADAS AL MÓDULO
'''
def add_training_info(film_name, recommend):
    line = get_film_info(film_name)
    
    #Si line=="" hubo un error.
    if line!="":
        line = line + recommend +"\n" 
        
        #Si no existe, lo crea.
        with open(training_data, "a+") as myfile:
            myfile.write(line)


'''
    FUNCIONES AUXILIARES.
'''

def get_film_info(name):
    
    info=get_movie_info(name)
    
    if(info['Response']=='False' or info['Rated']=='N/A'):
        print(info)
        return ""    
    
    line = ""
    
    if 'title' in parameters:
        line= line + info['Title'] + ","

    if 'director' in parameters:
        director=info['Director'].split(',')[0]
        line= line + director + ","  
        
    if 'Runtime' in parameters:
        runtime=info['Runtime'].split()[0]
        line= line + runtime + ","  
    
    genres=info['Genre'].split()
        
    if 'Genre' in parameters: 
        genre=genres[0].replace(',','')
        line= line + genre + ","      
    
    if 'Subgenre' in parameters:
        subgenre= genres[1].replace(',','')
        line= line + subgenre + ","       
    
    for x in info['Ratings']:
        if 'imdb' in parameters and x['Source']== 'Internet Movie Database':
            imdb_ratio=x['Value'].split('/')[0]
            line= line + imdb_ratio + ","  

        if 'metacritic' in parameters and x['Source']== 'Metacritic':
            metacritic_ratio=x['Value'].split('/')[0]
            line= line + metacritic_ratio + ","  

        if 'rotten' in parameters and x['Source']== 'Rotten Tomatoes':
            rotten_ratio=x['Value'].replace('%','')
            line= line + rotten_ratio + ","  
            
    return line



'''
    EJEMPLO DE FUNCIONAMIENTO
'''

if __name__ == "__main__":
    
    #Si no existe el fichero, añadimos la cabecera
    my_file = Path(training_data)
    
    if not my_file.is_file():
        
        #creamos el fichero si no existe y añadimos la cabecera
        line=""
        for x in parameters:
            line= line + str(x) +","
    
        line = line[:len(line)-1] + line[(len(line)+1):]+",recommend\n"
        
        with open(training_data, "w+") as myfile:
                   myfile.write(line)
    
    #Añadimos los ejemplos de entrenamiento.
    add_training_info('Alita','NO')
    add_training_info('Gladiator','YES')
    add_training_info('The Prestige','YES')
    add_training_info('Dunkirk','YES')
    add_training_info('Titanic','NO')
    add_training_info('Hateful eight','YES')
    add_training_info('Kingsman','YES')
    add_training_info('Harry Potter and the Chamber of Secrets','YES')
    add_training_info('Batman vs Superman','NO')
    add_training_info('Suicide Squad','NO')
    add_training_info('Hitman','NO')
    add_training_info('Kill Bill','YES')
    add_training_info('Django Unchained','YES')
    add_training_info('Black Panther','NO')
    add_training_info('Captain Marvel','NO')
    add_training_info('Thor Ragnarok','YES')
    add_training_info('Avengers Infinity War','YES')


    #Ver los resultados en el fichero marcado en training_data