import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración base de la aplicación"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'tu-clave-secreta-aqui-cambiala')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de modelos ML - ajustar rutas para Render
    if os.getenv('RENDER'):
        # En Render, los modelos están en la raíz del proyecto
        MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models'))
    else:
        # En desarrollo local
        MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models'))
    
    VECTORIZER_PATH = os.path.join(MODELS_DIR, 'vectorizer.pkl')
    SVM_MODEL_PATH = os.path.join(MODELS_DIR, 'svm_model.pkl')
    NB_MODEL_PATH = os.path.join(MODELS_DIR, 'nb_model.pkl')
    
    # Límites de caracteres
    MAX_TITLE_LENGTH = 200
    MAX_DESCRIPTION_LENGTH = 8000
    
    # Rate limiting
    RATE_LIMIT_REQUESTS = 20
    RATE_LIMIT_WINDOW = 5  # minutos

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    # En producción, usar SQLite si no hay DATABASE_URL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 