# -*- coding: utf-8 -*-


'''
    Módulo asociado al sistema de inferencia de recomendaciones 
'''


from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier, MultilayerPerceptronClassifier 
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.sql.types import IntegerType

from omdb_module import get_movie_info
from pathlib import Path


class Trained_Model:
    
    #Constructor.
    def __init__(self):
      
      
        '''
            PARÁMETROS ASOCIADOS A LA CONFIGURACIÓN DEL SISTEMA
        '''
          
        #Asociados a la sesión Spark.
        self.session_name="SparkML" 
        
        #Asociados al entrenamiento del modelo mediante SparkML.
        self.numeric_columns=['Runtime','metacritic','imdb','rotten']
        self.string_columns=['director','Genre','Subgenre','recommend']
        
        self.incomplete_sign='NULL'
        
        self.label_column="label"
        self.result_column="prediction"
        self.features_column="features"
        
        #En función del valor de este campo, utilizará una técnica u otra para entrenar el sistema.
        #Los posibles valores son regresión logística, árbol de clasificación y red neuronal.
        self.model_type="logistic_regression"
        
        #Parámetros que se utilizarán para el entrenamiento.
        self.parameters=['director','Runtime','Genre','Subgenre','metacritic','imdb','rotten']   #Nombre de las columnas (en orden) del fichero de entrenamiento/test que se van a utilizar en la tarea.
        
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
        #df=self.__set_types(df)
        
        df=self.__prepare_df(df)
        
        #En función del modelo seleccionado utilizará un tipo de aprendizaje u otro.
        if self.model_type== "logistic_regression":
            self.model=self.__train_with_logistic_regression(df)
            
        '''
        RELLENAR EL ELSE ---> TODO
        '''
    
    '''
        FUNCIONALIDADES PRINCIPALES DEL SISTEMA
    '''
    
    #Opinion es 'YES' o 'NO'
    def add_opinion(self,film_name, opinion):
        self.__add_training_info(film_name,opinion)
        
        
    #SUPONEMOS QUE LA PELÍCULA EXISTE
    
    '''
        
        Devuelve "" en caso de error.
        
        Devuelve YES o NO en caso contrario.
    '''
    def get_recommendation(self,film_name):
        
        #Obtenemos la línea que se escribirá en el test_data
        line = self.__get_film_info(film_name)
        
        #Si se ha encontrado la película...
        if line!="":
            line = line + "YES\n" #Añadimos el campo asociado a la recomendación. Su valor es irrelevante.
            
            #Sobreescribe el contenido de test_data
            self.__write_header(self.test_data)
            
            #Append con la cabecera
            with open(self.test_data, "a") as myfile:
                myfile.write(line)
                
            #Cargamos el contenido de test_data y lo parseamos.
            df=self.__load_df(self.test_data)
            df=self.__prepare_df(df)
            
            #Obtenemos las inferencias del sistema. "Predice" lo que diría el usuario.
            predictions = self.model.transform(df)
            
            #Devolvemos la recomendación.
            result=predictions.select('prediction').collect()[0]
            return self.__switch_label(result[self.result_column],result['label'])

        else:
            #Si no se ha encontrado la película, devolvemos "".
            return ""
        
    '''
        FUNCIONES AUXILIARES DEL SISTEMA
    '''
    
    def __switch_label(self, prediction,label):
        if prediction==label:
            return 'YES'
        else:
            return 'NO'

    '''
        Si hubo un error, devuelve "".
        Si no, devuelve "OK"
    '''
    
    def __add_training_info(self,film_name, recommend):
        line = self.__get_film_info(film_name)
        
        #Si line=="" hubo un error.
        if line!="":
            line = line + recommend +"\n" 
            
            #Si no existe, lo crea. Lo parsea.
            
            #Escribimos la cabecera.
            my_file = Path(self.training_data)
            if not my_file.is_file():
                self.__write_header(self.training_data)
            
            #Escribimos la línea.
            with open(self.training_data, "a") as myfile:
                myfile.write(line)
                
            #Si no hubo un error, se reentrena el modelo del sistema.
            df=self.__load_df(self.training_data)
            #df= self.__set_types(df)
            df=self.__prepare_df(df) 
            df.show()
            
            #Por ahora usa regresión logística.
            
            if self.model_type=="logistic_regression":
                self.model=self.__train_with_logistic_regression(df)
            else:
                print("TODO")
            '''
                TODO------------->
            '''
            
            return "OK"
        else:
            return ""
        
        
    def __load_file(self,filename):
        #Creamos la sesión del df.
        spark = SparkSession \
            .builder \
            .appName(self.session_name) \
            .getOrCreate()
    
        return spark.read.option("header", "true").option("inferSchema", "true").csv(filename)
    
    
    
    def __write_header(self,filename):
        line=""
        for x in self.parameters:
            line= line + str(x) +","
    
        line = line[:len(line)-1] + line[(len(line)+1):]+",recommend\n"
        with open(filename, "w+") as myfile:
                   myfile.write(line)
                   
    
    def __load_df(self,filename):
        #Si no existe lo creamos.
        my_file = Path(filename)
        
        if not my_file.is_file():
            #creamos el fichero si no existe y añadimos la cabecera
            self.__write_header(filename)
        
        
        df=self.__load_file(filename)   #Cargamos el dataframe.
        df=self.__filter_incomplete_instances(df) #Eliminamos las instancias incompletas (aquellas que contienen '?' en algún campo).
        
        df=self.__set_types(df)
        
        return df
    
    def __filter_incomplete_instances(self,df):
        for x in self.string_columns:
            df=df.filter(df[x]!=self.incomplete_sign)
        return df
    
    def __set_types(self,df):
        for x in self.numeric_columns:
            df=df.withColumn(x+"Tmp",df[x].cast(IntegerType())).drop(x).withColumnRenamed(x+"Tmp",x)
     
        return df
    
    #Devuelve el modelo entrenado.
    def __train_with_logistic_regression(self,df):
        lr = LogisticRegression(maxIter=self.max_iter)
        return lr.fit(df)
    
    #Devuelve el modelo entrenado.
    def __train_with_decision_tree(self,df):
        dt = DecisionTreeClassifier(maxBins=30000, labelCol="label", featuresCol="features")
        return dt.fit(df)
    
    def __train_with_multilayer_perceptrón_classifier(self,df,layers, max_iter, block_size, seed ):
        trainer = MultilayerPerceptronClassifier(maxIter=max_iter, layers=layers, blockSize=block_size, seed=seed)
        return trainer.fit(df)
    
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


    def __prepare_df(self,df):
        return Pipeline(stages=self.__prepare_dataframes_transformers()).fit(df).transform(df)
    
    def __get_film_info(self,name):
    
        info=get_movie_info(name)
        
        if(info['Response']=='False' or info['Rated']=='N/A'):
            return ""    
        
        line = ""
        
        if 'title' in self.parameters:
            line= line + info['Title'] + ","
    
        if 'director' in self.parameters:
            director=info['Director'].split(',')[0]
            line= line + director + ","  
            
        if 'Runtime' in self.parameters:
            runtime=info['Runtime'].split()[0]
            line= line + runtime + ","  
        
        genres=info['Genre'].split()
            
        if 'Genre' in self.parameters: 
            genre=genres[0].replace(',','')
            line= line + genre + ","      
        
        if 'Subgenre' in self.parameters:
            subgenre= genres[1].replace(',','')
            line= line + subgenre + ","       
        
        for x in info['Ratings']:
            if 'imdb' in self.parameters and x['Source']== 'Internet Movie Database':
                imdb_ratio=x['Value'].split('/')[0]
                line= line + imdb_ratio + ","  
    
            if 'metacritic' in self.parameters and x['Source']== 'Metacritic':
                metacritic_ratio=x['Value'].split('/')[0]
                line= line + metacritic_ratio + ","  
    
            if 'rotten' in self.parameters and x['Source']== 'Rotten Tomatoes':
                rotten_ratio=x['Value'].replace('%','')
                line= line + rotten_ratio + ","  
                
        return line
    
    
if __name__ == "__main__":
    tm=Trained_Model()

    print(tm.add_opinion('Django Unchained','YES'))    
    print(tm.add_opinion('Alita','NO'))
    
    print(tm.get_recommendation('Alita'))
    
    
    