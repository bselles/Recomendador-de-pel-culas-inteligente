# -*- coding: utf-8 -*-


"""
    PARA PROCESAR EL DATASET DE KAGGLE.COM    
"""

#from omdb_module import search_for_movie


filename= 'datasets/tmdb_5000_credits.csv'
output_filename= 'datasets/filmsdb'
with open(filename, "r") as myfile:
   #Obtenemos la línea asociada
   content=myfile.readlines()
   
   #Obtenemos de la línea, el nombre de la película.
   
for x in content:
   title=x.split(',')[1]
   
   try:
       '''
       #Buscamos el título en la base de datos de omdb
       title_result=search_for_movie(title)
       
       if title_result!="":
           #Si no hubo ningun error, escribimos el el fichero de salida.
           with open(output_filename, "a") as myfile:
               myfile.write(title_result+'\n')
       
       else:
           #Si hubo algún error.
           print('No se encontró la película '+ title)
   
       '''
       with open(output_filename, "a") as myfile:
           myfile.write(title+'\n')
   except:
       print('Exception here: '+title)
   
   



