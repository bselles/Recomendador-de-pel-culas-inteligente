# -*- coding: utf-8 -*-

'''
    Módulo controlador.
'''



from intent_recognition import recognize_intent
from omdb_module import get_movie_info, get_summary_plot, get_actors,get_director, get_awards,get_metacritic_score, get_imdb_score, get_rottentomatoes_score


#Variables globales

input="Which are the actors of Rambo?" #Pregunta introducida por el usuario.


intent, entity= recognize_intent(input)


if(entity==""):
    print("Entidad no encontrada")
else:
    if(intent=="ask_for_general_info"):
        print(get_movie_info(entity))
    elif(intent=="ask_for_plot"):
        print(get_summary_plot(entity))
    elif(intent=="ask_for_actors"):
        print(get_actors(entity))
    elif(intent=="ask_for_director"):
        print(get_director(entity))
    elif(intent=="ask_for_awards"):
        print(get_awards(entity))
    elif(intent=="ask_for_metacritic_score"):
        print(get_metacritic_score(entity))
    elif(intent=="ask_for_imdb_score"):
        print(get_imdb_score(entity))
    elif(intent=="ask_for_rotten_score"):
        print(get_rottentomatoes_score(entity))
    elif(intent=="as_for_score"):
        #print(get_movie_info(entity))
        print("MOSTRARIA NOTAS")
    else:
        print("El intent no se ha encontrado correctamente")


