import sys
import os
from typing import Tuple, Optional, Any

def setup_ml_imports():
    """Configurar imports para modelos ML"""
    # Permite importar desde la carpeta ml/
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ml_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'ml'))
    if ml_path not in sys.path:
        sys.path.append(ml_path)

def load_ml_models():
    """Cargar todos los modelos de ML"""
    setup_ml_imports()
    
    try:
        from preprocess import preprocesar_texto, cargar_vectorizador, vectorizar_texto
        from predict import cargar_modelo, predecir
        
        # Importar configuración
        from config.settings import Config
        
        # Cargar modelos
        vectorizer = cargar_vectorizador(Config.VECTORIZER_PATH)
        svm_modelo = cargar_modelo(Config.SVM_MODEL_PATH)
        nb_modelo = cargar_modelo(Config.NB_MODEL_PATH)
        
        # Intentar cargar SaBERT
        try:
            from sabert_model import cargar_modelo_sabert, predecir_sabert
            modelo_sabert, tokenizer_sabert = cargar_modelo_sabert()
        except Exception as e:
            print(f"Error cargando SaBERT: {e}")
            modelo_sabert = None
            tokenizer_sabert = None
        
        return {
            'vectorizer': vectorizer,
            'svm_modelo': svm_modelo,
            'nb_modelo': nb_modelo,
            'modelo_sabert': modelo_sabert,
            'tokenizer_sabert': tokenizer_sabert,
            'preprocesar_texto': preprocesar_texto,
            'vectorizar_texto': vectorizar_texto,
            'predecir': predecir,
            'predecir_sabert': predecir_sabert if modelo_sabert else None
        }
        
    except Exception as e:
        print(f"Error cargando modelos ML: {e}")
        return None

class MLPredictor:
    """Clase para manejar predicciones de ML"""
    
    def __init__(self, models_dict):
        self.models = models_dict
        self.vectorizer = models_dict.get('vectorizer')
        self.svm_modelo = models_dict.get('svm_modelo')
        self.nb_modelo = models_dict.get('nb_modelo')
        self.modelo_sabert = models_dict.get('modelo_sabert')
        self.tokenizer_sabert = models_dict.get('tokenizer_sabert')
        self.preprocesar_texto = models_dict.get('preprocesar_texto')
        self.vectorizar_texto = models_dict.get('vectorizar_texto')
        self.predecir = models_dict.get('predecir')
        self.predecir_sabert = models_dict.get('predecir_sabert')
    
    def predict_svm(self, texto: str) -> Tuple[int, float]:
        """Realizar predicción con SVM"""
        if not all([self.vectorizer, self.svm_modelo, self.preprocesar_texto, self.vectorizar_texto]):
            raise ValueError("Modelo SVM no disponible")
        
        texto_proc = self.preprocesar_texto(texto)
        vector = self.vectorizar_texto(self.vectorizer, texto_proc)
        pred = self.predecir(self.svm_modelo, vector)
        
        # Calcular confianza
        try:
            if hasattr(self.svm_modelo, "predict_proba"):
                prob = self.svm_modelo.predict_proba(vector)[0]
                confianza = max(prob) * 100
            else:
                decision = self.svm_modelo.decision_function(vector)[0]
                confianza = min(95, max(55, abs(decision) * 20 + 60))
        except:
            confianza = 75.0
        
        return pred, confianza
    
    def predict_nb(self, texto: str) -> Tuple[int, float]:
        """Realizar predicción con Naive Bayes"""
        if not all([self.vectorizer, self.nb_modelo, self.preprocesar_texto, self.vectorizar_texto]):
            raise ValueError("Modelo Naive Bayes no disponible")
        
        texto_proc = self.preprocesar_texto(texto)
        vector = self.vectorizar_texto(self.vectorizer, texto_proc)
        pred = self.predecir(self.nb_modelo, vector)
        
        # Calcular confianza
        try:
            if hasattr(self.nb_modelo, "predict_proba"):
                prob = self.nb_modelo.predict_proba(vector)[0]
                confianza = max(prob) * 100
            else:
                confianza = 75.0
        except:
            confianza = 75.0
        
        return pred, confianza
    
    def predict_sabert(self, texto: str) -> Tuple[int, float]:
        """Realizar predicción con SaBERT"""
        if not all([self.modelo_sabert, self.tokenizer_sabert, self.predecir_sabert]):
            raise ValueError("Modelo SaBERT no disponible")
        
        pred, probs = self.predecir_sabert(self.modelo_sabert, self.tokenizer_sabert, texto)
        confianza = max(probs) * 100
        
        return pred, confianza 