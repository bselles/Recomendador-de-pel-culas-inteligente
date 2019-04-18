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

'''
    1- OBTENER EL TÍTULO ASOCIADO A UNA PELÍCULA
    
    Dada una cadena de caracteres introducida por el usuario que representa el título de una película,
    devuelve el título asociado a esta película que figura en la base de datos de OMDB.
    
    Input:
        -title: cadena de caracteres que representa el título de la película del cual se quiere obtener el título en IMDB.
    
    Output:
        Una cadena de caracteres que puede valer:
            -"" si hubo algún error.
            -El título almacenado en la base de datos OMDB.

'''
def search_for_movie(title):
    title=parse_blank_spaces(title)
    info=urllib.request.urlopen(omdb_endpoint + omdb_apikey + "&s="+title).read() 
    
    result= parse_bytes_to_JSON(info)
    
    if result['Response']=='True':
        return result['Search'][0]['Title']
    else:
        return ""  #Si devuelve "", implica que hubo un error.
   

'''
    2- OBTENER INFORMACIÓN SOBRE UNA PELÍCULA
    
    Dada una cadena de caracteres que representa el título de una película, interactua con la base de datos de OMDB y obtiene información 
    sobre la película.
    
    Input:
        -title: cadena de caracteres que representa el título de la película.
    
    Output:
        un objeto JSON con toda la información asociada a la película. 
        
        Para ver si la operación sucedió correctamente, consultar el campo 'Response' del objeto JSON resultante. En el caso de que aparezca algún error,
        valdrá 'False'. Si no, si todo ha ido correctamente, valdrá 'True'.
    
'''
def get_movie_info(title):
    
    title=parse_blank_spaces(title) #Añadimos '%20' en los espacios en blanco para lanzar el mensaje GET
    
    #Añadimos la opción con la trama sin resumir.
    info=urllib.request.urlopen(omdb_endpoint + omdb_apikey + "&t="+ parse_blank_spaces(title)+"&plot=full").read() 
    
    #Versión con la trama resumida.
    #info=urllib.request.urlopen(omdb_endpoint + omdb_apikey + "&t="+title).read() 
    
    return parse_bytes_to_JSON(info)


'''
    3- EXTRAER LA NOTA ASOCIADA A ROTTEN TOMATOES
    
    Dada una cierta información sobre una película extraída mediante la funcionalidad descrita anteriormente (obtención de información sobre una película),
    parsea la información y extrae la nota que esa película tiene asociada en la página https://www.rottentomatoes.com/ (Rotten Tomatoes).
    
    Input:
        -Info: objeto json resultante de una llamada a la funcionalidad de obtención de información sobre una película de este módulo.
        
    Output:
        -Una cadena de caracteres que representa la nota que esa película tiene asociada en RT.
    
'''

def get_rottentomatoes_score(info):
    
    for x in info['Ratings']:
        if (x['Source'] == 'Rotten Tomatoes' ):
            return x['Value'].replace('%','') 



'''
    FUNCIONES AUXILIARES
'''

#---------------------------------------------------------------------------
'''
    Dado un objeto en tipo bytes, obtenemos el objeto JSON asociado (si este tenía forma de JSON)
    
    Se utiliza para parsear los resultados de las llamadas a la API de OMDB.
    
    Input:
        -data: resultado a la llamada de la API OMDB
        
    Output:
        objeto JSON con el contenido de data formateado
'''
def parse_bytes_to_JSON(data):
    decoded = data.decode('utf8') #Decodificamos usando utf-8. El resultado es un string con forma de json.
    return json.loads(decoded);  #Creamos el json a partir del string  

'''
    Dada una cadena de caracteres, introduce "%20" en los espacios en blanco.
    
    Se utiliza para formatear las cadenas de caracteres que se introducen en el mensaje GET cuando se realizan 
    llamadas a la API OMDB.
'''
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

