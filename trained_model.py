# -*- coding: utf-8 -*-


'''
    Módulo asociado al sistema de inferencia de recomendaciones 
    
    Este módulo contiene la clase que representa el modelo de aprendizaje del sistema. Dicho de otra forma,
    este módulo almacena la clase que se encargará de aprender a partir de los gustos del usuario para realizar
    mejores recomendaciones.
    
    Para ello, utiliza las opiniones que el usuario ha introducido previamente. Cada vez que el usuario da una opinión sobre 
    una película (si le ha gustado o no), el sistema busca información sobre dicha película y analiza distintas características 
    de la película como su duración, el género, su director, etc para ver qué ha determinado que le guste o no.
    
    El sistema, para lograr su aprendizaje, aplica algoritmos de Aprendizaje Automático sobre las opiniones introducidas por el usuario
    (y las correspondientes características asociadas a la película). Actualmente, el sistema soporta 4 métodos:
        
        1-Aprendizaje mediante clustering (algoritmo kNN).
        2-Aprendizaje mediante un árbol de clasificación.
        3-Aprendizaje mediante regresión logística.
        4-Aprendizaje mediante el uso de una red neuronal.
        
    Para seleccionar un tipo de aprendizaje u otro, se debe indicar el tipo deseado en el parámetro (atributo de la clase) "model_type".
    
'''

#Imports necesarios para el funcionamiento del sistema.
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier, MultilayerPerceptronClassifier 
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.sql.types import IntegerType

from pathlib import Path
from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017')
db = client.recomendadorpeliculas 


class Trained_Model:
    
    #Constructor.
    def __init__(self):      
        '''
            PARÁMETROS ASOCIADOS A LA CONFIGURACIÓN DEL SISTEMA
        '''
          
        #Asociados a la sesión Spark.
        self.session_name="SparkML"  #Nombre de la sesión de Spark
        
        #Asociados al entrenamiento del modelo mediante SparkML.
        
        #Parámetros que se utilizarán para el entrenamiento.
        
        '''
        Deben seguir el siguiente orden (aparezcan o no):
        title, director,Runtime, Genre,Subgenre, imdb,rotten,metacritic.
        En función del orden en el que se ubiquen en la lista, aparecerán escritos en la cabecera de los ficheros de una forma u otra.
        '''
        
        self.parameters=['director','Runtime','Genre','Subgenre','imdb','rotten','metacritic']   #Nombre de las columnas (en orden) del fichero de entrenamiento/test que se van a utilizar en la tarea.        
        
        self.numeric_columns=['Runtime','imdb','rotten','metacritic']         #Parámetros numericos que se van a utilizar.
        self.string_columns=['director','Genre','Subgenre','recommend']       #Parámetros no numericos (cadenas de caracteres) que se van a utilizar en el entrenamiento del modelo.
        
        self.incomplete_sign='NULL'         #Símbolo que identifica las posiciones del datafraque no tienen ningún valor. 
        
        self.label_column="label"           #Nombre de la columna del dataframe asociada a la etiqueta (label)
        self.result_column="prediction"     #Nombre de la columna del dataframe asociada a la predicción realizada por el sistema.
        self.features_column="features"     #Nombre de la columna que almacenará el vector de características que utilizará el sistema para su aprendizaje.
        
        #En función del valor de este campo, utilizará una técnica u otra para entrenar el sistema.
        
        '''
            POSIBLES VALORES:
                1.Red neuronal: neural_net
                2.Árbol de decisión: classification_tree
                3.Clustering mediante kNN: clustering
                4.Regresion logística: logistic_regression
        '''
        
        self.model_type="clustering"
        
       
        #Nombre del fichero dónde de almacenarán los ejemplos de entrenamiento.
        self.training_data= "file.train"                                       
        
        #Nombre del fichero dónde se almacenarán los ejemplos de test.
        self.test_data="file.test" 
        
        #Número de iteraciones que se realizarán en el aprendizaje.
        self.max_iter=100
        
        '''
            APRENDIZAJE INICIAL DEL SISTEMA
        '''
        
        df=self.__load_df(self.training_data) #Cargamos los ejemplos de entrenamiento del sistema.
        df=self.__prepare_df(df)    #Realizamos las transformaciones necesarias al df cargado para que el sistema lo pueda usar para aprender.
        
        #En función del modelo seleccionado utilizará un tipo de aprendizaje u otro.
        if self.model_type== "logistic_regression":
            self.model=self.__train_with_logistic_regression(df)
        elif self.model_type == "classification_tree":
            self.model = self.__train_with_decision_tree(df)
        elif self.model_type == "neural_net":
            self.model = self.__train_with_multilayer_perceptron_classifier(df,[len(self.parameters), 5,4, 2], self.max_iter, 128, 1234)
        elif self.model_type == "clustering":
            self.model = self.__train_with_clustering(df)
        
    
    '''
        FUNCIONALIDADES PRINCIPALES DEL SISTEMA
    '''
    
    '''
        1- AÑADIR LA OPINIÓN DEL USUARIO
        
        Dado el nombre de una película y si le ha gustado al usuario (YES/NO), el sistema utiliza esta nueva información para entrenar 
        su modelo de aprendizaje. De esta forma, analiza las caracteristicas de la película para determinar el peso de cada factor a la 
        hora de determinar la opinión del usuario y así realizar mejores recomendaciones en el futuro.
        
        Input:
            - film_name: cadena de caracteres que representa el nombre de la película.
            - opinion: cadena de caracteres que representa la opinión del usuario. Puede valer YES o NO.
    
    
        Output:
            -Cadena de caracteres cuyo valor puede ser:
                - "" en el caso de que haya ocurrido algún error.
                - "OK" en el caso de que no haya ningún error.
    '''
    def add_opinion(self,film_name, opinion):
        return self.__add_training_info(film_name,opinion)
        
    
    '''       
        2- OBTENER UNA RECOMENDACIÓN POR PARTE DEL SISTEMA
    
        Dado el nombre de una película, el sistema, utilizando todo lo que ha aprendido previamente, indica si la recomendaría o no.
        
        Input:
            -film_name: cadena de caracteres que representa el nombre de la película.
            
        Output:
            Devuelve una cadena de caracteres cuyo valor puede ser:
                -"" en el caso de que haya sucedido algún error.
                -"NO" en el caso de que el sistema infiera que no debe recomendar la película introducida.
                -"YES" en el caso de que el sistema infiera que debe recomendar la película introducida.
    '''
    
    def get_recommendation(self,film_name):    
        #Obtenemos la línea que se escribirá en el test_data
        line = self.__get_film_info(film_name)
        #Si se ha encontrado la película...
        if line!="":
            df= self.__load_df(self.training_data) #Cargamos el dataframe que usamos para inferir la recomendación
            line = line + "NO\n" #Añadimos el campo asociado a la recomendación. Su valor es irrelevante
            
            #Reescribimos el fichero de test.
            self.__write_header(self.test_data)
            
            #Escribimos el ejemplo que queremos predecir.
            with open(self.test_data, "a") as myfile:
                myfile.write(line)
            
            #Lo unimos a los casos previos para obtener una predicción más precisa.
            df1= self.__load_df(self.test_data)
            df=df.union(df1)
            df=self.__prepare_df(df) #Realizamos las modificaciones oportunas para que se pueda procesar el df.
            
            #Obtenemos las inferencias del sistema. "Predice" lo que diría el usuario.
            predictions = self.model.transform(df)

            #Posición en la que se va ubicar la predicción del ejemplo que nos interesa.            
            pos= len(predictions.select('recommend').collect())-1
                        
            #Devolvemos la recomendación.Devolvemos la que se encuentra el la última posición.
            return self.__switch_label(predictions.select('recommend').collect()[pos]['recommend'] \
                                       , predictions.select('prediction').collect()[pos][self.result_column]\
                                       ,predictions.select(self.label_column).collect()[pos][self.label_column])
            
        else:
            #Si no se ha encontrado la película (si ha sucedido algún error), devolvemos "".
            return ""
        
    '''
        FUNCIONES AUXILIARES DEL SISTEMA
    '''


    '''
        Dada la predicción que realiza el sistema, la etiqueta asociada a la predicción y etiqueta del entrenamiento devuelve
        si el sistema infiere que se debe recomendar la película o no.
        
        Input:
            -recommend: etiqueta asociada al entrenamiento.
            -prediction: predicción realizada por el sistema.
            -label: etiqueta asociada a la predicción.
    
        Output:
            cadena de caracteres cuyo valor puede ser 'YES' o 'NO'
    
    
    '''
    
    def __switch_label(self, recommend,prediction,label):
        if prediction==label:
            return recommend
        else:
            if(recommend=='YES'):
                return 'NO'
            else:
                return 'YES'

    '''
        Dado el nombre de una película y si le ha gustado o no al usuario (YES/NO), añade esta opinión (y la información
        asociada a esa película) a los datos que usa el modelo del sistema para entrenarse y aprender.
    
        Input:
            -film_name: nombre de la película.
            -recommend: cadena de caracteres cuyo valor sea 'YES' o 'NO'.
                
        Output:
            "" en el caso de que haya algún error.
            'OK' en caso contrario.
    '''

    def __add_training_info(self,film_name, recommend):
        line = self.__get_film_info(film_name)
        #Si line=="" hubo un error.
        if line!="":
            line = line + recommend +"\n" 
            
            #Si no existe, crea el fichero de entrenamiento.
            if not Path(self.training_data).is_file():
                #Escribimos la cabecera.
                self.__write_header(self.training_data)
            
            #Escribimos la línea.
            with open(self.training_data, "a") as myfile:
                myfile.write(line)
                
            #Si no hubo un error, se reentrena el modelo del sistema.
            df=self.__load_df(self.training_data)
            df=self.__prepare_df(df) #Transforma el df para que sea apto para el aprendizaje.
            
            #En función del tipo de entrenamiento seleccionado, realizará uno u otro.
            if self.model_type=="logistic_regression":
                self.model=self.__train_with_logistic_regression(df)
            elif self.model_type == "classification_tree":
               self.model = self.__train_with_decision_tree(df)
            elif self.model_type == "neural_net":
                self.model = self.__train_with_multilayer_perceptron_classifier(df, [ len(self.parameters), 5,4, 2], self.max_iter, 128, 1234)
            elif self.model_type == "clustering":
                self.model = self.__train_with_clustering(df)
            
            return "OK"
        else:
            return ""
        
    '''
        Dado un fichero csv, crea un df sin formatear.
    '''
    def __load_file(self,filename):
        #Creamos la sesión del df.
        self.spark_session = SparkSession \
            .builder \
            .appName(self.session_name) \
            .getOrCreate()
    
        return self.spark_session.read.option("header", "true").csv(filename)
    
    
    '''
        Dado un fichero, añade la cabecera asociada a los parámetros que utiliza el modelo para entrenar al sistema. Estos parámetros son los que aparecen en self.parameters.
    '''
    def __write_header(self,filename):
        line=""
        for x in self.parameters:
            line= line + str(x) +","
    
        line = line[:len(line)-1] + line[(len(line)+1):]+",recommend\n"
        with open(filename, "w+") as myfile:
                   myfile.write(line)
                   
    '''
        Dado un fichero csv, crea un spark Dataframe eliminando las instancias incompletas (que tienen NULL en alguna posición) y lo procesa para eliminar errores de 
        tipos.
    '''
    def __load_df(self,filename):
        #Si no existe lo creamos.
        my_file = Path(filename)
        
        if not my_file.is_file():
            #creamos el fichero si no existe y añadimos la cabecera
            self.__write_header(filename)
        
        
        df=self.__load_file(filename)   #Cargamos el dataframe.
        df=self.__filter_incomplete_instances(df) #Eliminamos las instancias incompletas.
        df=self.__set_types(df)
        
        return df
    
    
    '''
        Dado un dataframe, elimina las instancias incompletas. Las instancias incompletas son aquellas que contiene  self.incomplete_sign.
    '''
    def __filter_incomplete_instances(self,df):
        for x in self.string_columns:
            df=df.filter(df[x]!=self.incomplete_sign)
        return df
    
    '''
        Dado un dataframe, elimina las incompatibilidades de tipos. Asocia los tipos correspondientes a cada columna.
    '''
    def __set_types(self,df):
        for x in self.numeric_columns:
            df=df.withColumn(x+"Tmp",df[x].cast(IntegerType())).drop(x).withColumnRenamed(x+"Tmp",x)
     
        return df
    
    '''
        Dado un dataframe, entrena un modelo que utiliza regresión logística para inferir recomendaciones.
        
        Devuelve un modelo entrenado con los datos proporcionados que se usará en el futuro para realizar 
        recomendaciones.
    '''
    def __train_with_logistic_regression(self,df):
        lr = LogisticRegression(maxIter=self.max_iter, labelCol="label", featuresCol="features")
        return lr.fit(df)
    
    '''
        Dado un dataframe, entrena un modelo que utiliza un árbol de clasificación para inferir recomendaciones.
        
        Devuelve un modelo entrenado con los datos proporcionados que se usará en el futuro para realizar 
        recomendaciones.
    '''    
    def __train_with_decision_tree(self,df):
        dt = DecisionTreeClassifier(maxBins=30000, labelCol="label", featuresCol="features")
        return dt.fit(df)

    '''
        Dado un dataframe, entrena un modelo que utiliza una red neuronal para inferir recomendaciones.
        
        Devuelve un modelo entrenado con los datos proporcionados que se usará en el futuro para realizar 
        recomendaciones.
    ''' 
    def __train_with_multilayer_perceptron_classifier(self,df,layers, max_iter, block_size, seed, labelCol="label", featuresCol="features" ):
        trainer = MultilayerPerceptronClassifier(maxIter=max_iter, layers=layers, blockSize=block_size, seed=seed)
        return trainer.fit(df)
    
    '''
        Dado un dataframe, entrena un modelo que utiliza clústering con el algoritmo KNN para inferir recomendaciones.
        
        Devuelve un modelo entrenado con los datos proporcionados que se usará en el futuro para realizar 
        recomendaciones.
    ''' 
    
    def __train_with_clustering(self,df):
        kmeans = KMeans().setK(2).setSeed(1)
        return kmeans.fit(df)
    
    
    '''
        En función de los parámetros que tiene el sistema en su configuración, prepara una lista de transformadores que se utilizarán
        en la transformación del dataframe.
    '''
    def __prepare_dataframes_transformers(self):
        transformers_list=[]
        input_cols_va=[]
        
        for x in range(len(self.string_columns)): #Solo pondremos un StringIndexer para las colúmnas no numéricas.
            if len(self.string_columns)-1== x:
                transformers_list.append(StringIndexer(inputCol=self.string_columns[len(self.string_columns)-1], outputCol=self.label_column))
            else:
                transformers_list.append( StringIndexer(inputCol=self.string_columns[x], outputCol=("i_"+self.string_columns[x])))
                input_cols_va.append("i_"+self.string_columns[x])
        
        input_cols_va=input_cols_va + self.numeric_columns
        
        transformers_list.append( VectorAssembler(inputCols=input_cols_va, outputCol=self.features_column))
        
        return transformers_list


    '''
        Dado un dataframe, aplica los transformadores para procesarlo y dar lugar a un df afín a los modelos que se usarán para entrenar al sistema.
    '''
    def __prepare_df(self,df):
        return Pipeline(stages=self.__prepare_dataframes_transformers()).fit(df).transform(df)
    
    
    '''
        Dado el nombre de una película, devuelve una línea con la información necesaria para el aprendizaje del sistema. Esta información
        tendrá más o menos aspectos en función de los parámetros que aparezcan en self.parameters.
        
        Devuelve "" en el caso de que suceda algún error.
        
    '''
    def __get_film_info(self,name):
    
        #info=get_movie_info(name)
        info=self.__get_film_info_db(name)
        
        if(info==""):
            return ""
        
        line = ""
        
        if 'title' in self.parameters:
            line= line + info['Title'] + ","
    
        if 'director' in self.parameters:
            director=info['Director']
            line= line + director + ","  
            
        if 'Runtime' in self.parameters:
            runtime=info['Runtime']
            line= line + str(runtime) + ","  
        
        genres=info['Genre']
        
        if 'Genre' in self.parameters: 
            genre = genres[0]
            line= line + genre + ","      
        
        if 'Subgenre' in self.parameters:
            subgenre=genres[1]
            line= line + subgenre + ","       
        
        if 'imdb' in self.parameters :
            imdb_ratio=info['Internet Movie Database']
            line= line + str(imdb_ratio) + "," 
            
        if 'metacritic' in self.parameters :
            metacritic_ratio=info['Metacritic']
            line= line + str(metacritic_ratio) + ","  
        
        if 'rotten' in self.parameters :
            rotten_ratio=info['Rotten Tomatoes']
            line= line + str(rotten_ratio) + ","
                
        return line  
    
    def __get_film_info_db(self,name):
        
        myquery = { "Title": name }
        
        mydoc = list(db.peliculas.find(myquery))
        
        if(len(mydoc)==0):
            return ""
        
        return mydoc[0]
    
'''
    EJEMPLO DE FUNCIONAMIENTO DEL MÓDULO
'''
if __name__ == "__main__":
    tm=Trained_Model()
    
    print(tm.add_opinion('Hidalgo','YES'))
    print(tm.add_opinion('Avatar','NO'))
    print(tm.get_recommendation('Hidalgo'))

