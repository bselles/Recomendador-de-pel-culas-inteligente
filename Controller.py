# -*- coding: utf-8 -*-

'''
    Módulo controlador.
'''


from intent_recognition import recognize_intent
from omdb_module import get_movie_info, get_summary_plot, get_actors,get_director, get_awards,get_metacritic_score, get_imdb_score, get_rottentomatoes_score
from trained_model import Trained_Model

#Variables globales


tm=Trained_Model()


ftr=['Avatar','Looper','Her','War', 'Warcraft']



while True:
    example= input('Insert here:  ')
    
    intent, entity= recognize_intent(example)
    
    print(intent)
    if(entity=="" and intent!="ask_for_recommendation"):
        entity=input("Which film you're talking about:  ")
        
    
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
    elif(intent=="not_good_opinion"):
        tm.add_opinion(entity,'NO')        
    elif(intent=="good_opinion"):
        tm.add_opinion(entity,'YES')
    elif(intent=="ask_for_recommendation"):
        
        i=0
        while(i<len(ftr)):
            if('YES'== tm.get_recommendation(ftr[i])):
                print(ftr[i])
                i=len(ftr)
            i=i+1
        
        
        
        
    elif(intent=="ask_for_score"):
        #print(get_movie_info(entity))
        print("MOSTRARIA NOTAS")
    else:
        print("El intent no se ha encontrado correctamente")
    
    
