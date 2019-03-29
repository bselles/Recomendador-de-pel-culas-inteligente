# -*- coding: utf-8 -*-

'''
    Módulo que implementa la comunicación con la API de OMDB (Open Movie Database)
'''

#Imports correspondientes
import urllib.request
import json

omdb_endpoint='http://www.omdbapi.com/?apikey='
omdb_apikey='dad4d84f'

#---------------------------------------------------------------------------
#Necesario para el parseo de 
def parse_bytes_to_JSON(input):
    decoded = input.decode('utf8') #Decodificamos usando utf-8. El resultado es un string con forma de json.
    return json.loads(decoded);  #Creamos el json a partir del string  

def parse_blank_spaces(input):
    #Si no tenemos una sola palabra, parsea. En caso contrario, no hace nada.
    return input.replace(" ", "%20") 

#---------------------------------------------------------------------------


def get_movie_info(title):
    title=parse_blank_spaces(title)
    #Añadimos la opción con la trama sin resumir.
    info=urllib.request.urlopen(omdb_endpoint + omdb_apikey + "&t="+title+"&plot=full").read() 
    #Versión con la trama resumida.
    #info=urllib.request.urlopen(omdb_endpoint + omdb_apikey + "&t="+title).read() 
    return parse_bytes_to_JSON(info)
    


def get_summary_plot(title):
    info=get_movie_info(title)
    return info['Plot']


def get_actors(title):
    info=get_movie_info(title)
    return info['Actors']

def get_director(title):
    info=get_movie_info(title)
    return info['Director']

def get_awards(title):
    info=get_movie_info(title)
    return info['Awards']

def get_production(title):
    info=get_movie_info(title)
    return info['Production']

def get_metacritic_score(title):
    info=get_movie_info(title)
    return info['Metascore']

def get_imdb_score(title):
    info=get_movie_info(title)
    return info['imdbRating']

def get_rottentomatoes_score(title):
    info=get_movie_info(title)
    
    for x in info['Ratings']:
        if (x['Source'] == 'Rotten Tomatoes' ):
            return x['Value']
    

#print(get_movie_info('Gladiator'))
#print(get_summary_plot('Gladiator'))
#print(get_actors('Gladiator'))
#print(get_director('Gladiator'))
#print(get_awards('Gladiator'))
#print(get_production('Gladiator'))
#print(get_metacritic_score('Gladiator'))
#print(get_imdb_score('Gladiator'))
#print(get_rottentomatoes_score('Gladiator'))

