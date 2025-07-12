from flask import Flask
from flask_login import LoginManager
from models.database import db, User
from utils.ml_models import load_ml_models, MLPredictor
from config.settings import config
import os

def create_app(config_name='default'):
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Configurar Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'error'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Cargar modelos ML
    print("Cargando modelos de Machine Learning...")
    models_dict = load_ml_models()
    if models_dict:
        ml_predictor = MLPredictor(models_dict)
        print("✅ Modelos cargados exitosamente")
    else:
        ml_predictor = None
        print("❌ Error cargando modelos ML")
    
    # Registrar blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp, set_ml_predictor
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    
    # Establecer predictor ML global
    set_ml_predictor(ml_predictor)
    
    # Crear tablas de base de datos
    with app.app_context():
        db.create_all()
        print("✅ Base de datos inicializada")
    
    return app

def main():
    """Función principal para ejecutar la aplicación"""
    # Determinar configuración basada en variable de entorno
    config_name = os.getenv('FLASK_ENV', 'default')
    if config_name == 'production':
        config_name = 'production'
    else:
        config_name = 'development'
    
    app = create_app(config_name)
    
    print(f"🚀 Iniciando FactCheck AI en modo {config_name}")
    print(f"📊 Modelos disponibles: SVM, Naive Bayes, SaBERT")
    
    # Usar el puerto de la variable de entorno PORT (Render usa 10000 por defecto)
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 Servidor iniciado en http://0.0.0.0:{port}")
    
    app.run(debug=app.config.get('DEBUG', True), 
            host="0.0.0.0", 
            port=port)

if __name__ == "__main__":
    main()