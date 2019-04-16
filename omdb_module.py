# -*- coding: utf-8 -*-

'''
    MÓDULO DE INTERACCIÓN CON LA FUENTE DE CONOCIMIENTO
    
    Módulo que implementa la comunicación con la API de OMDB (Open Movie Database).
    Mediante la comunicación con esta API, se obtendrá nueva información que si procede
    se introducirá en la base de conocimiento.
'''

'''
    PARÁMETROS DE CONFIGURACIÓN DEL MÓDULO
'''

omdb_endpoint='http://www.omdbapi.com/?apikey='
omdb_apikey='dad4d84f'



#Imports correspondientes
import urllib.request
import json


'''
    FUNCIONALIDADES DEL MÓDULO
'''


#Devuelve el título de la película que más se parece a lo que ha introducido el usuario.
def search_for_movie(title):
    title=parse_blank_spaces(title)
    info=urllib.request.urlopen(omdb_endpoint + omdb_apikey + "&s="+title).read() 
    
    result= parse_bytes_to_JSON(info)
    
    if result['Response']=='True':
        return result['Search'][0]['Title']
    else:
        return ""
    #Si devuelve "", implica que ubo un error.


def get_movie_info(title):
    #Se supone que el título introducido ya es válido.
    title=parse_blank_spaces(title)

    #Buscamos la película que más se parece a lo que ha introducido el usuario.
    #movie=search_for_movie(title)  
    
    #print(movie)
    
    #Si se obtuvo alguna respuesta
    '''
    if movie['Response'] == 'True':
        #Añadimos la opción con la trama sin resumir.
        info=urllib.request.urlopen(omdb_endpoint + omdb_apikey + "&t="+ parse_blank_spaces(movie['Search'][0]['Title'])+"&plot=full").read() 
        #Versión con la trama resumida.
        #info=urllib.request.urlopen(omdb_endpoint + omdb_apikey + "&t="+title).read() 
        return parse_bytes_to_JSON(info)
    else:
        return ""
    '''
    
    #Añadimos la opción con la trama sin resumir.
    info=urllib.request.urlopen(omdb_endpoint + omdb_apikey + "&t="+ parse_blank_spaces(title)+"&plot=full").read() 
    #Versión con la trama resumida.
    #info=urllib.request.urlopen(omdb_endpoint + omdb_apikey + "&t="+title).read() 
    return parse_bytes_to_JSON(info)

def get_rottentomatoes_score(info):
    
    for x in info['Ratings']:
        if (x['Source'] == 'Rotten Tomatoes' ):
            return x['Value'].replace('%','')

'''
    FUNCIONES AUXILIARES
'''

#---------------------------------------------------------------------------
#Necesario para el parseo de 
def parse_bytes_to_JSON(data):
    decoded = data.decode('utf8') #Decodificamos usando utf-8. El resultado es un string con forma de json.
    return json.loads(decoded);  #Creamos el json a partir del string  

def parse_blank_spaces(data):
    #Si no tenemos una sola palabra, parsea. En caso contrario, no hace nada.
    return data.replace(" ", "%20") 

#---------------------------------------------------------------------------


'''
    EJEMPLO DE FUNCIONAMIENTO DEL MÓDULO
'''
if __name__ == "__main__":
    print(get_movie_info('Gladiator'))
    #print(search_for_movie('Gladiator'))
    #print(get_rottentomatoes_score('Gladiator'))

