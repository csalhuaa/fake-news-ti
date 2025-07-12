import joblib
import os

def cargar_modelo(path):
    return joblib.load(path)

def predecir(modelo, vector):
    pred = modelo.predict(vector)
    return int(pred[0])