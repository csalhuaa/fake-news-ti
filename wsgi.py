import os
import sys

# Agregar el directorio flask-template al path
current_dir = os.path.dirname(os.path.abspath(__file__))
flask_template_dir = os.path.join(current_dir, 'flask-template')
sys.path.insert(0, flask_template_dir)

# Importar la aplicación Flask
from app import create_app

# Crear la aplicación para producción
app = create_app('production')

if __name__ == "__main__":
    # Usar el puerto de la variable de entorno PORT (Render usa 10000 por defecto)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)