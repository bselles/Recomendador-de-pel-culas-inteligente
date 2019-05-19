# -*- coding: utf-8 -*-

'''
    Parámetros que utilizará el sistema para su funcionamiento

'''


'''
Técnica que el modelo entrenado utilizará para su aprendizaje

POSIBLES VALORES:
    1.Red neuronal: neural_net
    2.Árbol de decisión: classification_tree
    3.Clustering mediante kNN: clustering
    4.Regresion logística: logistic_regression
'''

model_type="clustering"  

'''
Asociados al entrenamiento del modelo mediante SparkML.

Parámetros que se utilizarán para el entrenamiento.

Deben seguir el siguiente orden (aparezcan o no):
title, director,Runtime, Genre,Subgenre, imdb,rotten,metacritic.
En función del orden en el que se ubiquen en la lista, aparecerán escritos en la cabecera de los ficheros de una forma u otra.
'''

parameters=['director','Runtime','Genre','Subgenre','imdb','rotten','metacritic']   #Nombre de las columnas (en orden) del fichero de entrenamiento/test que se van a utilizar en la tarea.        

numeric_columns=['Runtime','imdb','rotten','metacritic']         #Parámetros numericos que se van a utilizar.
string_columns=['director','Genre','Subgenre','recommend']       #Parámetros no numericos (cadenas de caracteres) que se van a utilizar en el entrenamiento del modelo.

incomplete_sign='NULL'         #Símbolo que identifica las posiciones del datafraque no tienen ningún valor. 

label_column="label"           #Nombre de la columna del dataframe asociada a la etiqueta (label)
result_column="prediction"     #Nombre de la columna del dataframe asociada a la predicción realizada por el sistema.
features_column="features"     #Nombre de la columna que almacenará el vector de características que utilizará el sistema para su aprendizaje.