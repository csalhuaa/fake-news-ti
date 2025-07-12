from transformers import BertForSequenceClassification, BertTokenizer
import torch

# Cargar modelo y tokenizer una sola vez
def cargar_modelo_sabert():
    model = BertForSequenceClassification.from_pretrained("VerificadoProfesional/SaBERT-Spanish-Fake-News")
    tokenizer = BertTokenizer.from_pretrained("VerificadoProfesional/SaBERT-Spanish-Fake-News")
    return model, tokenizer

# Ejecutar inferencia detallada
def predecir_sabert(modelo, tokenizer, texto, threshold=0.5):
    inputs = tokenizer(texto, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = modelo(**inputs)
    
    logits = outputs.logits
    probs = torch.softmax(logits, dim=1).squeeze().tolist()
    pred_index = int(torch.argmax(logits, dim=1).item())

    # Aplicar umbral si quieres ser más estricto
    if probs[pred_index] < threshold and pred_index == 1:
        pred_index = 0  # bajamos a falsa si no supera threshold

    return pred_index, probs
