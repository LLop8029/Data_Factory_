from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

cliente=MongoClient("mongodb+srv://larisalopez8029:ouKBE8hpk448OrRh@cluster0.yu0xlvv.mongodb.net/?retryWrites=true&w=majority")

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

data=cliente.sample_restaurants
collection=data.restaurants

find=collection.find()
datos=pd.DataFrame(list(find))


st.title("Base de Datos listing en MongoDB")
st.text("### Larisa López Payán")

st.write("## Data from MongoDB Atlas:")
st.write(datos.head())

st.write("## Number of cuisine Type")
cuisine_type=datos["cuisine"].value_counts().sort_values(ascending=False)

st.bar_chart(cuisine_type)

st.write("## Number of borough")
borough=datos["borough"].value_counts().sort_values(ascending=False)

st.bar_chart(borough)

streamlit.run("c:/Users/caqso/OneDrive/Escritorio/MDC/Semestre 2/Programaciòn ll/Mongo_LILP_py.py")