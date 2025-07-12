from preprocess import preprocesar_texto, cargar_vectorizador, vectorizar_texto

# Prueba de limpieza y stopwords
texto = "El presidente del Gobierno reitera el compromiso de España con la UE."
print("Texto limpio:", preprocesar_texto(texto))

# Prueba de vectorización (ajusta la ruta a tu vectorizer.pkl real)
vectorizer = cargar_vectorizador("../models/vectorizer.pkl")
vector = vectorizar_texto(vectorizer, preprocesar_texto(texto))
print("Vector shape:", vector.shape)