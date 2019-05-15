# -*- coding: utf-8 -*-


from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017')
db = client.recomendadorpeliculas            

myquery = { "Title": "Hidalgo" }

mydoc = db.peliculas.find(myquery)

for x in list(mydoc):
  print(x)