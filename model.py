# -*- coding: utf-8 -*-


'''
    MODULO ASOCIADO AL MODELO ENTRENADO POR EL SISTEMA.
'''

from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier, MultilayerPerceptronClassifier 
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.sql.types import IntegerType

#from model_trainer import parameters, training_data, test_data
from omdb_module import get_movie_info
from pathlib import Path

'''
    PARAMETROS DE CONFIGURACIÓN DEL MÓDULO
'''

session_name="SparkML" 
numeric_columns=['Runtime','metacritic','imdb','rotten']
string_columns=['director','Genre','Subgenre','recommend']
incomplete_sign='NULL'
label_column="label"
result_column="prediction"
features_column="features"
model_type="logistic_regression"

#Asociadas al entrenamiento.
parameters=['director','Runtime','Genre','Subgenre','metacritic','imdb','rotten']   #Nombre de las columnas (en orden) del fichero de entrenamiento/test que se van a utilizar en la tarea.
training_data= "file.train"                                                         #Localización/nombre del fichero con los ejemplos de entrenamiento.
test_data="file.test"                                                               #Localización/nombre del fichero con los ejemplos de testing del modelo.


max_iter=100

def set_types(df):
    
    for x in numeric_columns:
        df=df.withColumn(x+"Tmp",df[x].cast(IntegerType())).drop(x).withColumnRenamed(x+"Tmp",x)
 
    return df

'''
    VARIABLES GLOBALES DEL MÓDULO
'''
    #Entrenamos el modelo de forma predeterminada
    
df=load_df(training_data)
df=set_types(df)

        
df= prepare_df(df) 
        
#Por ahora usa regresión logística.
model=train_with_logistic_regression(df,max_iter) 



'''
    FUNCIONALIDADES ASOCIADAS AL MÓDULO
'''

def add_training_info(film_name, recommend):
    line = get_film_info(film_name)
    
    #Si line=="" hubo un error.
    if line!="":
        line = line + recommend +"\n" 
        
        #Si no existe, lo crea.
        with open(training_data, "a+") as myfile:
            myfile.write(line)
            
        #Si no hubo un error, se reentrena el modelo del sistema.
        df=load_df(training_data)
        
        df= set_types(df)
        
        df= prepare_df(df) 
        
        df.show()
        
        #Por ahora usa regresión logística.
        model=train_with_logistic_regression(df,max_iter)
        
                
#SUPONEMOS QUE LA PELÍCULA EXISTE
def get_recommendation(film_name):
    line = get_film_info(film_name)
    if line!="":
        line = line + "YES\n" 
        
        #Si no existe, lo crea.
        with open(test_data, "a+") as myfile:
            myfile.write(line)
            
        df=load_df(test_data)
        df=prepare_df(df)
                
        predictions = model.transform(df)
        
        predictions.show()



'''
    FUNCIONES AUXILIARES DEL MÓDULO
'''
def get_film_info(name):
    
    info=get_movie_info(name)
    
    if(info['Response']=='False' or info['Rated']=='N/A'):
        return ""    
    
    line = ""
    
    if 'title' in parameters:
        line= line + info['Title'] + ","

    if 'director' in parameters:
        director=info['Director'].split(',')[0]
        line= line + director + ","  
        
    if 'Runtime' in parameters:
        runtime=info['Runtime'].split()[0]
        line= line + runtime + ","  
    
    genres=info['Genre'].split()
        
    if 'Genre' in parameters: 
        genre=genres[0].replace(',','')
        line= line + genre + ","      
    
    if 'Subgenre' in parameters:
        subgenre= genres[1].replace(',','')
        line= line + subgenre + ","       
    
    for x in info['Ratings']:
        if 'imdb' in parameters and x['Source']== 'Internet Movie Database':
            imdb_ratio=x['Value'].split('/')[0]
            line= line + imdb_ratio + ","  

        if 'metacritic' in parameters and x['Source']== 'Metacritic':
            metacritic_ratio=x['Value'].split('/')[0]
            line= line + metacritic_ratio + ","  

        if 'rotten' in parameters and x['Source']== 'Rotten Tomatoes':
            rotten_ratio=x['Value'].replace('%','')
            line= line + rotten_ratio + ","  
            
    return line


def load_file(filename):
    #Creamos la sesión del df.
    spark = SparkSession \
        .builder \
        .appName(session_name) \
        .getOrCreate()

    return spark.read.option("header", "true").option("inferSchema", "true").csv(filename)


def load_df(filename):
    
    #Si no existe lo creamos.
    my_file = Path(filename)
    
    if not my_file.is_file():
        
        #creamos el fichero si no existe y añadimos la cabecera
        line=""
        for x in parameters:
            line= line + str(x) +","
    
        line = line[:len(line)-1] + line[(len(line)+1):]+",recommend\n"
        
        with open(filename, "w+") as myfile:
                   myfile.write(line)
    
    
    df=load_file(filename)   #Cargamos el dataframe.
    df=filter_incomplete_instances(df) #Eliminamos las instancias incompletas (aquellas que contienen '?' en algún campo).
    
    return df

def filter_incomplete_instances(df):
    for x in string_columns:
        df=df.filter(df[x]!=incomplete_sign)
    return df


def prepare_dataframes_transformers():
    transformers_list=[]
    input_cols_va=[]
    
    for x in range(len(string_columns)): #Solo pondremos un StringIndexer para las colúmnas no numéricas.
        if len(string_columns)-1== x:
            transformers_list.append(StringIndexer(inputCol=string_columns[len(string_columns)-1], outputCol=label_column))
        else:
            transformers_list.append( StringIndexer(inputCol=string_columns[x], outputCol=("i_"+string_columns[x])))
            input_cols_va.append("i_"+string_columns[x])
    
    input_cols_va=input_cols_va + numeric_columns
    
    transformers_list.append( VectorAssembler(inputCols=input_cols_va, outputCol=features_column))
    
    return transformers_list


def prepare_df(df):
    return Pipeline(stages=prepare_dataframes_transformers()).fit(df).transform(df)


#Devuelve el modelo entrenado.
def train_with_logistic_regression(df, max_iter):
    lr = LogisticRegression(maxIter=max_iter)
    return lr.fit(df)

#Devuelve el modelo entrenado.
def train_with_decision_tree(df):
    dt = DecisionTreeClassifier(maxBins=30000, labelCol="label", featuresCol="features")
    return dt.fit(df)

def train_with_multilayer_perceptrón_classifier(df,layers, max_iter, block_size, seed ):
    trainer = MultilayerPerceptronClassifier(maxIter=max_iter, layers=layers, blockSize=block_size, seed=seed)
    return trainer.fit(df)


def test_model(test_file, model):
    #Cargamos el contenido del test_file.
    df=load_df(test_file)
    df = df.withColumn("rottenTmp", df.rotten.cast(IntegerType())).drop("rotten").withColumnRenamed("rottenTmp", "rotten")
    df=prepare_df(df)    
    predictions = model.transform(df)    
    evaluator = MulticlassClassificationEvaluator(
        labelCol=label_column, predictionCol=result_column, metricName="accuracy")
    return evaluator.evaluate(predictions) #Devolvemos la precisión obtenida.





if __name__ == "__main__":
    '''
    df=load_df(training_data)
    
    #Cambiar rotten...
    df = df.withColumn("rottenTmp", df.rotten.cast(IntegerType())).drop("rotten").withColumnRenamed("rottenTmp", "rotten")
    
    
    df= prepare_df(df) 
    print(df)
    
    max_iter=100
    
    lr=train_with_logistic_regression(df,max_iter)
    
    print(str(test_model(training_data,lr)))      
    
    dt=train_with_decision_tree(df)
    print(str(test_model(training_data,dt)))      

    rn=train_with_multilayer_perceptrón_classifier(df,[len(parameters), 10, 10, 2], 100, 128, 1234 )
    print(str(test_model(training_data,rn)))
    '''
    
    #Si no existe el fichero, añadimos la cabecera
    my_file = Path(training_data)
    
    if not my_file.is_file():
        
        #creamos el fichero si no existe y añadimos la cabecera
        line=""
        for x in parameters:
            line= line + str(x) +","
    
        line = line[:len(line)-1] + line[(len(line)+1):]+",recommend\n"
        
        with open(training_data, "w+") as myfile:
                   myfile.write(line)
                   
                   
    #Para testing data
    my_file = Path(test_data)
    
    if not my_file.is_file():
        
        #creamos el fichero si no existe y añadimos la cabecera
        line=""
        for x in parameters:
            line= line + str(x) +","
    
        line = line[:len(line)-1] + line[(len(line)+1):]+",recommend\n"
        
        with open(test_data, "w+") as myfile:
                   myfile.write(line)
    
    
    
    
    add_training_info('Alita','NO')
    add_training_info('Gladiator','YES')
    add_training_info('The Prestige','YES')
    add_training_info('Dunkirk','YES')
    add_training_info('Titanic','NO')
    add_training_info('Hateful eight','YES')
    add_training_info('Kingsman','YES')
    add_training_info('Harry Potter and the Chamber of Secrets','YES')
    add_training_info('Batman vs Superman','NO')
    add_training_info('Suicide Squad','NO')
    add_training_info('Hitman','NO')
    add_training_info('Kill Bill','YES')
    add_training_info('Django Unchained','YES')
    add_training_info('Black Panther','NO')
    add_training_info('Captain Marvel','NO')
    add_training_info('Thor Ragnarok','YES')
    add_training_info('Avengers Infinity War','YES')


    get_recommendation('Django Unchained')
    
    
    
#------------------



