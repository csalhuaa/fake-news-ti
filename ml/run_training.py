import pandas as pd
import joblib
from preprocess import preprocesar_texto
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from train import entrenar_y_guardar_modelos
import os

# 1. Cargar datos
df = pd.read_csv("../data/raw/D57000_complete.csv")
df = df.dropna(subset=["title", "description", "label"])

# 2. Unir título y descripción
df["texto"] = df["title"].astype(str) + " " + df["description"].astype(str)

# 3. Preprocesar textos
df["texto_proc"] = df["texto"].apply(preprocesar_texto)

# 4. Vectorizar
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df["texto_proc"])
y = df["label"].astype(int)

# 5. Guardar vectorizador
os.makedirs("../models", exist_ok=True)
joblib.dump(vectorizer, "../models/vectorizer.pkl")

# 6. Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 7. Entrenar y guardar modelos
entrenar_y_guardar_modelos(X_train, y_train, "../models")

print("Entrenamiento completo. Modelos y vectorizador guardados en ../models/")