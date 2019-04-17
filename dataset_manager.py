# -*- coding: utf-8 -*-


"""
    Script en python para procesar el dataset de Kaggle.com con 5000 películas de TMDB
    
    Enlace de descarga del dataset: https://www.kaggle.com/tmdb/tmdb-movie-metadata 
    
    Este script, extrae los nombres de las películas que aparecen en el dataset.
    
    Estas, serán las 5000 películas que nuestro sistema podrá recomendar al usuario.    
"""

filename= 'datasets/tmdb_5000_credits.csv'
output_filename= 'datasets/filmsdb'

#Leemos el contenido del dataset.
with open(filename, "r") as myfile:
   #Obtenemos la línea asociada
   content=myfile.readlines()
   
#Obtenemos de la línea, el nombre de la película.
for x in content:
   title=x.split(',')[1]
   
   try:
       with open(output_filename, "a") as myfile:
           myfile.write(title+'\n')
   except:
       print('Exception here: '+title)
   
   



