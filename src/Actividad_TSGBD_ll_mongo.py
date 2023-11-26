#importar librerias necesarias
import pandas as pd
import json
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import streamlit as st
import matplotlib.pyplot as plt

#Enlazar con mongoDB para base de datos.
cliente=MongoClient("mongodb+srv://larisalopez8029:ouKBE8hpk448OrRh@cluster0.yu0xlvv.mongodb.net/?retryWrites=true&w=majority")

#Enlazar y crear base de datos mediante pandas.
data=cliente.prueba
collection=data.db1
find=collection.find()
data_1=pd.DataFrame(list(find))


collection=data.db2
find_2=collection.find()
data_2=pd.DataFrame(list(find_2))


#lectura y carga de base de datos mediante pandas.
#data_1=pd.read_csv("C:/Users/caqso/OneDrive/Escritorio/db1.csv",encoding='latin-1')
#data_2=pd.read_csv("C:/Users/caqso/OneDrive/Escritorio/db2.csv",encoding='latin-1')

collection=data.config
find_3=list(collection.find())
doc_json=json.dumps(find_3,default=str)
log_file=find_3

collection=data.users
find_4=list(collection.find())
doc_json_1=json.dumps(find_4,default=str)
users=json.loads(doc_json_1)

collection=data.db1j
find_6=list(collection.find())
data_22=find_6

collection=data.db2j
find_5=list(collection.find())
data_11=find_5


#Carga de datos en json.
#with open('C:/Users/caqso/OneDrive/Escritorio/config.json') as f:
 #   log_file = json.load(f)

# Carga archivo JSON de usuarios.
#with open("C:/Users/caqso/OneDrive/Escritorio/users.json", "r") as archivo:
#    users = json.load(archivo)


def buscar_business_name(archivo,profile):
   with open(archivo, "r") as archivo:
      data=json.load(archivo)
      business_name=[]
      for key, value in data.items():
         if "level" in value and value["level"]==profile:
            business_name.append(value["business_name"])

      return business_name


def extract_node_names(archivo, profile):
        with open(archivo, "r") as file:
            data = json.load(file)    
        node_names = []
        for key, value in data.items():
            if "level" in value and value["level"] == profile:
                node_names.append(key)
        return node_names

def save_log(user, action, data_requested=None):
    
    # Definir datos a agregar al archivo json.
    new_data = {"action": action, "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

    # Agregar los datos de accesos en los nuevos datos.
    if (action == "success_db_check" or action == "unsuccess_db_check" ) and data_requested is not None:
        new_data["data_accessed"] = data_requested

    # Especificar ruta de archivo json.
    json_file_path = doc_json

    # Leer datos existentes del archivo JSON (si corresponde).
    existing_data = {}
    try:
        with open(json_file_path) as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        # Si el archivo aún no existe, manejaremos la excepción e inicializaremos los datos como un diccionario vacío.
        pass

    # Obtenga los valores de "action" y "timestamp" de los nuevos datos.
    action_value = new_data["action"]
    timestamp_value = new_data["timestamp"]

    # Comprobar si el usuario existe en los datos existentes.
    if user in existing_data:
        # Comprobar si existe la clave "activities" e inicializar si no existe.
        if "activities" in existing_data[user]:
            existing_data[user]["activities"].append(new_data)
        else:
            existing_data[user]["activities"] = [new_data]
    else:
        # Si el usuario no existe, crea una nueva entrada con la acción.
        existing_data[user] = {"activities": [new_data]}


    # Guarde los datos actualizados en el archivo json.
    with open(doc_json) as f:
        json.dump(existing_data, f, indent=4)

nombre = input("Por favor, ingresa tu nombre: ")
actions = ['login','unsucessful_login','success_db_check','unsuccess_db_check']

# Verifica si el nombre de usuario está en el json.
if nombre in users:
    # Obtiene el valor de "profile" asociado al nombre de usuario.
    save_log(nombre, actions[0])
    archivo_usuarios = users
    with open(archivo_usuarios, "r") as file:
        data = json.load(file)
    profile = data[nombre]["profile"]
    print(f"Hola {nombre} !!, tu perfil es: {profile}")
    columna_consulta = input("\n Que columna quieres consultar? ")

    # Extraer nombres de nodos de db1.json
    node_names_data_1 = extract_node_names(data_11, profile)
    # Extraer nombres de nodos dem db2.json
    node_names_data_2 = extract_node_names(data_22, profile)
    
    if columna_consulta in node_names_data_1:
        save_log(nombre, actions[2],columna_consulta)
        print(f'Claro {nombre}, aqui tienes la información de {columna_consulta} \n\n')
        print(data_1.loc[:, columna_consulta].head())
    elif columna_consulta in node_names_data_2:
        save_log(nombre, actions[2],columna_consulta)
        print(f'Claro {nombre}, aqui tienes la información de {columna_consulta} \n\n')
        print(data_2.loc[:, columna_consulta].head())
    else:
        save_log(nombre, actions[3],columna_consulta)
        print(f'Ese dato {columna_consulta} no existe en la base de datos')

else:
    save_log(nombre, actions[1])
    print(f"Lo siento {nombre} , no se encontró tu nombre en la base de Usuarios.")