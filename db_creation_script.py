# -*- coding: utf-8 -*-

films_list="./datasets/films"
films_names="./datasets/films_names"


'''
    Nombre de la base de datos: recomendadorpeliculas
    Coleccion: películas

'''

#Imports correspondientes
from omdb_module import search_for_movie, get_movie_info
from pymongo import MongoClient

'''
    SCRIPT PARA OBTENER LA INFORMACIÓN DE LAS PELÍCULAS DEL DATASET E INTRODUCIRLO EN LA BASE DE DATOS.
'''

client = MongoClient('mongodb://127.0.0.1:27017')
db = client.recomendadorpeliculas


result=[]

with open(films_names, 'w+') as fw:
    with open(films_list, "r") as f:
        films = f.readlines()
        cont=1
        for film in films:
            x={}
            
            try:
              title=search_for_movie(film)
              if title!="":
                  info=get_movie_info(title)
                  if info!="": 
                      x['Title']=info['Title']       #STRING
                      x['Year']= int(info['Year'])   #NUM
                      x['Runtime']=int(info['Runtime'].split(" ")[0])  #NUM
                      x['Plot']= info['Plot']
                      x['Awards']=info['Awards']
                      x['Released']=info['Released']
                      ratings=info['Ratings']
                      
                      for item in ratings:
                          tmp=""
                          for value in item.values():
                              if(tmp==""):
                                  tmp=value
                              else:
                                  x[tmp]=float(value.split('/')[0].split('%')[0])
                                  tmp=""
    
                              
                      
                      genres=info['Genre'].split(',')
                      
                      genres_result=[]
                      for y in genres:
                          if y[0]==' ':
                              genres_result.append(y[1:])
                          else:
                              genres_result.append(y)
            
                      x['Genre']=genres_result
                      
                      
                      x['Director']=info['Director']
                      actors_result=[]
                      actors=info['Actors'].split(',')
                      
                      for y in actors:
                          if y[0]==' ':
                              actors_result.append(y[1:])
                          else:
                              actors_result.append(y)
    
                      x['Actors']=actors_result
                      x['id']= cont
                      print(cont)
                      #print(str(x))
                      cont=cont+1
                      db.peliculas.insert_one(x)
                      fw.write(x['Title']+'\n')
            except Exception as e:
                print ("Ha sucedido un error con la película ", film, " :", e)       

print("DONE")
