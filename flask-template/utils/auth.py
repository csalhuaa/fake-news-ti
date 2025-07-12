from flask_bcrypt import Bcrypt
from functools import wraps
from datetime import datetime, timedelta
from flask import request, jsonify, current_app

bcrypt = Bcrypt()

# Diccionario simple para rate limiting
request_counts = {}

def rate_limit(max_requests=None, window_minutes=None):
    """Decorador para limitar el número de requests por usuario/IP"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Usar configuración por defecto si no se especifica
            max_req = max_requests or current_app.config.get('RATE_LIMIT_REQUESTS', 20)
            window = window_minutes or current_app.config.get('RATE_LIMIT_WINDOW', 5)
            
            # Identificar usuario (autenticado o IP)
            from flask_login import current_user
            if current_user.is_authenticated:
                key = f"user_{current_user.id}"
            else:
                key = f"ip_{request.remote_addr}"
            
            now = datetime.now()
            if key not in request_counts:
                request_counts[key] = []
            
            # Limpiar requests antiguos
            request_counts[key] = [req_time for req_time in request_counts[key] 
                                 if now - req_time < timedelta(minutes=window)]
            
            if len(request_counts[key]) >= max_req:
                return jsonify({
                    "success": False,
                    "error": f"Demasiadas solicitudes. Intenta de nuevo en {window} minuto(s)."
                }), 429
            
            request_counts[key].append(now)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_input_length(title, description, max_title=None, max_description=None):
    """Validar longitud de entrada"""
    max_title_len = max_title or current_app.config.get('MAX_TITLE_LENGTH', 200)
    max_desc_len = max_description or current_app.config.get('MAX_DESCRIPTION_LENGTH', 8000)
    
    if len(title) > max_title_len:
        return False, f"El título no puede exceder {max_title_len} caracteres"
    
    if len(description) > max_desc_len:
        return False, f"El contenido no puede exceder {max_desc_len} caracteres"
    
    return True, None 