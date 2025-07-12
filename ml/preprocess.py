import re
import string
import joblib
import os
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('stopwords', quiet=True)
STOPWORDS_ES = set(stopwords.words('spanish'))

def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r"http\S+", "", texto)
    texto = re.sub(r"[^a-záéíóúñü\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

def eliminar_stopwords(texto):
    return " ".join([palabra for palabra in texto.split() if palabra not in STOPWORDS_ES])

def preprocesar_texto(texto):
    texto = limpiar_texto(texto)
    texto = eliminar_stopwords(texto)
    return texto

def cargar_vectorizador(path):
    return joblib.load(path)

def vectorizar_texto(vectorizer, texto):
    return vectorizer.transform([texto])