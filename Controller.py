# -*- coding: utf-8 -*-

'''
    Módulo controlador.
'''


from intent_recognition import recognize_intent
from omdb_module import get_movie_info, get_summary_plot, get_actors,get_director, get_awards,get_metacritic_score, get_imdb_score, get_rottentomatoes_score
from trained_model import Trained_Model

#Variables globales


tm=Trained_Model()


ftr=['Avatar','Looper','Her','War', 'Warcraft', 'Dunkirk', 'The Prestige']

recommended_movies={} #Películas que ya han sido recomendadas.
not_to_recomend={}

def procesa(intent, entity):
    if(intent=="ask_for_general_info"):
        return get_movie_info(entity)
    elif(intent=="ask_for_plot"):
        return get_summary_plot(entity)
    elif(intent=="ask_for_actors"):
        return get_actors(entity)
    elif(intent=="ask_for_director"):
        return get_director(entity)
    elif(intent=="ask_for_awards"):
        return get_awards(entity)
    elif(intent=="ask_for_metacritic_score"):
        return get_metacritic_score(entity)
    elif(intent=="ask_for_imdb_score"):
        return get_imdb_score(entity)
    elif(intent=="ask_for_rotten_score"):
        return get_rottentomatoes_score(entity)
    elif(intent=="not_good_opinion"):
        not_to_recomend[entity]=True
        tm.add_opinion(entity,'NO')
        return "Thanks for giving your opinon"
    elif(intent=="good_opinion"):
        tm.add_opinion(entity,'YES')
        return "Thanks for giving your opinon"
    elif(intent=="ask_for_recommendation"):
        
        i=0
        resul = ""
        while(i<len(ftr)  ):
            if('YES'== tm.get_recommendation(ftr[i]) and not (ftr[i] in recommended_movies) and not(ftr[i] in not_to_recomend) ):
                recommended_movies[ftr[i]]=True
                resul = resul + ftr[i] + "\n"
                i=len(ftr)
            i=i+1
        return resul

    elif(intent=="ask_for_score"):
        #return get_movie_info(entity))
        return "MOSTRARIA NOTAS"
    else:
        return "El intent no se ha encontrado correctamente"



if __name__ == "__main__" :

    while True:
        example= input('Insert here: \n')
    
        intent, entity= recognize_intent(example)
    
        print(intent)
        if(entity=="" and intent!="ask_for_recommendation"):
            entity=input("Which film are you talking about?  \n")
        
        print(procesa(intent, entity))
    

    
    
