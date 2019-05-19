# -*- coding: utf-8 -*-
"""
Created on Wed May 15 20:12:47 2019

@author: Bielo
"""

from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017')
db = client.recomendadorpeliculas 


def __get_info_from_db(name):        
    return list(db.peliculas.find({ "Title": name }))[0]
    
def __get_films_by_genre(genre):
    return list(db.peliculas.find({ "Genre": genre }))

def __get_films_by_director(director):
    return list(db.peliculas.find({ "Director": director }))

def __get_films_by_actor(actor):
    return list(db.peliculas.find({ "Actors": actor }))

def __get_films_by_Runtime( runtime):
    if runtime=="short":
        query= { "Runtime": { '$lt': 61 } }
    elif runtime=="medium":
        query={ '$and': [ { "Runtime": { '$lt': 120 } }, { "Runtime": { '$gt': 60 } }  ]  } 
    elif runtime=="large":
        query= { "Runtime": { '$gt': 120 } }

    return list(db.peliculas.find( query ))


#print(__get_films_by_genre('Drama'))

#print(__get_films_by_director('Christopher Nolan'))

#print(__get_films_by_actor('Russell Crowe'))

print(__get_films_by_Runtime('large'))