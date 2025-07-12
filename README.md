# FactCheck AI - Detector de Fake News

Aplicación web para detectar noticias falsas utilizando inteligencia artificial avanzada.

## 🚀 Características

- **Modelos de IA**: SVM, Naive Bayes y SaBERT
- **Sistema de usuarios**: Registro, login y perfiles personalizados
- **Control de acceso**: Usuarios registrados acceden a modelos avanzados
- **Historial de análisis**: Seguimiento de predicciones realizadas
- **Interfaz moderna**: Diseño responsive con animaciones
- **Rate limiting**: Protección contra spam
- **Validación robusta**: Límites de caracteres y validaciones de entrada

## 📁 Estructura del Proyecto

```
flask-template/
├── config/                 # Configuración de la aplicación
│   ├── __init__.py
│   └── settings.py        # Configuraciones por entorno
├── models/                # Modelos de base de datos
│   ├── __init__.py
│   └── database.py        # Modelos User y Analysis
├── routes/                # Rutas de la aplicación
│   ├── __init__.py
│   ├── auth.py           # Rutas de autenticación
│   └── main.py           # Rutas principales
├── utils/                 # Utilidades
│   ├── __init__.py
│   ├── auth.py           # Utilidades de autenticación
│   └── ml_models.py      # Manejo de modelos ML
├── static/                # Archivos estáticos
│   ├── css/
│   └── js/
├── templates/             # Templates HTML
├── app.py                # Aplicación principal
├── requirements.txt      # Dependencias
└── .env                  # Variables de entorno
```

## 🛠️ Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd flask-template
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # o
   venv\Scripts\activate     # Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   Crear archivo `.env`:
   ```env
   SECRET_KEY=tu-clave-secreta-super-segura-aqui-cambiala
   DATABASE_URL=url-db
   FLASK_ENV=development
   ```

5. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

## 🔧 Configuración

### Variables de Entorno

- `SECRET_KEY`: Clave secreta para sesiones Flask
- `DATABASE_URL`: URL de conexión a PostgreSQL
- `FLASK_ENV`: Entorno de ejecución (development/production)

### Configuraciones por Entorno

- **Development**: Modo debug activado, logs detallados
- **Production**: Modo optimizado, sin debug

## 📊 Modelos de IA

### Modelos Disponibles

1. **SVM (Support Vector Machine)**
   - Rápido y eficiente
   - Bueno para textos cortos
   - Disponible para todos los usuarios

2. **Naive Bayes**
   - Análisis probabilístico
   - Bueno para análisis general
   - Disponible para todos los usuarios

3. **SaBERT**
   - Modelo avanzado basado en BERT
   - Especializado en español
   - Solo para usuarios registrados

### Límites de Caracteres

- **Título**: Máximo 200 caracteres
- **Contenido**: Máximo 8000 caracteres

## 🔐 Autenticación

### Funcionalidades de Usuario

- **Registro**: Crear cuenta nueva
- **Login**: Iniciar sesión con username/email
- **Perfil**: Ver estadísticas y historial
- **Editar perfil**: Modificar datos personales
- **Logout**: Cerrar sesión

### Control de Acceso

- **Invitados**: Solo SVM y Naive Bayes
- **Usuarios registrados**: Todos los modelos + historial

## 🚀 API Endpoints

### Endpoints Principales

- `GET /` - Página principal
- `GET /about` - Página acerca de
- `POST /predict` - Análisis de noticias
- `GET /api/health` - Estado de la API
- `GET /api/stats` - Estadísticas generales

## 🎨 Interfaz de Usuario

### Características

- **Diseño responsive**: Adaptable a todos los dispositivos
- **Animaciones**: Transiciones suaves y efectos visuales
- **Feedback visual**: Contadores de caracteres en tiempo real
- **Accesibilidad**: Navegación por teclado y focus visible
- **Mensajes flash**: Notificaciones de éxito/error

### Navegación por Teclado

- `Ctrl + Enter`: Enviar formulario de análisis
- `Escape`: Limpiar formulario
- `Tab`: Navegación entre elementos

## 🔒 Seguridad

### Medidas Implementadas

- **Rate limiting**: 20 requests por 5 minutos
- **Validación de entrada**: Límites de caracteres y sanitización
- **Contraseñas hasheadas**: Bcrypt para encriptación
- **Sesiones seguras**: Flask-Login para manejo de sesiones
- **CORS**: Configuración de seguridad para APIs

## 📈 Monitoreo

### Endpoints de Estado

- `/api/health`: Verificar estado de la aplicación
- `/api/stats`: Estadísticas de uso

### Logs

- Carga de modelos ML
- Errores de predicción
- Operaciones de base de datos

## 🚀 Despliegue

### Requisitos de Producción

- Python 3.8+
- PostgreSQL
- Memoria RAM: 2GB+ (para modelos ML)
- CPU: 2 cores+ (recomendado)

### Variables de Producción

```env
FLASK_ENV=production
SECRET_KEY=clave-super-segura-de-produccion
DATABASE_URL=url-de-produccion
```

