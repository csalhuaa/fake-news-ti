from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.database import db, User, Analysis
from utils.auth import rate_limit, validate_input_length
from utils.ml_models import MLPredictor
from config.settings import Config

main_bp = Blueprint('main', __name__)

# Variable global para el predictor ML (se inicializará en create_app)
ml_predictor = None

def set_ml_predictor(predictor):
    """Establecer el predictor ML global"""
    global ml_predictor
    ml_predictor = predictor

@main_bp.route("/")
def home():
    """Página principal"""
    return render_template("home.html")

@main_bp.route("/about")
def about():
    """Página acerca de"""
    return render_template("about.html")

@main_bp.route("/profile")
@login_required
def profile():
    """Página de perfil del usuario"""
    # Obtener estadísticas del usuario
    total_analyses = Analysis.query.filter_by(user_id=current_user.id).count()
    true_analyses = Analysis.query.filter_by(user_id=current_user.id, is_true=True).count()
    false_analyses = Analysis.query.filter_by(user_id=current_user.id, is_true=False).count()
    
    # Obtener análisis recientes
    recent_analyses = Analysis.query.filter_by(user_id=current_user.id)\
        .order_by(Analysis.created_at.desc()).limit(10).all()
    
    return render_template("profile.html", 
                         total_analyses=total_analyses,
                         true_analyses=true_analyses,
                         false_analyses=false_analyses,
                         recent_analyses=recent_analyses)

@main_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    """Editar perfil del usuario"""
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        
        # Validaciones básicas
        if not username or not email:
            flash("Usuario y email son requeridos", "error")
            return render_template("edit_profile.html")
        
        # Verificar si el username ya existe (excluyendo el usuario actual)
        existing_user = User.query.filter(
            User.username == username,
            User.id != current_user.id
        ).first()
        if existing_user:
            flash("El nombre de usuario ya está en uso", "error")
            return render_template("edit_profile.html")
        
        # Verificar si el email ya existe (excluyendo el usuario actual)
        existing_email = User.query.filter(
            User.email == email,
            User.id != current_user.id
        ).first()
        if existing_email:
            flash("El email ya está registrado", "error")
            return render_template("edit_profile.html")
        
        # Actualizar datos básicos
        current_user.username = username
        current_user.email = email
        
        # Cambiar contraseña si se proporciona
        if new_password:
            if not current_password:
                flash("Debes ingresar tu contraseña actual para cambiarla", "error")
                return render_template("edit_profile.html")
            
            if not current_user.check_password(current_password):
                flash("La contraseña actual es incorrecta", "error")
                return render_template("edit_profile.html")
            
            if new_password != confirm_password:
                flash("Las nuevas contraseñas no coinciden", "error")
                return render_template("edit_profile.html")
            
            if len(new_password) < 6:
                flash("La nueva contraseña debe tener al menos 6 caracteres", "error")
                return render_template("edit_profile.html")
            
            current_user.set_password(new_password)
        
        try:
            db.session.commit()
            flash("Perfil actualizado exitosamente", "success")
            return redirect(url_for("main.profile"))
        except Exception as e:
            db.session.rollback()
            flash("Error al actualizar el perfil. Por favor intenta de nuevo.", "error")
            return render_template("edit_profile.html")
    
    return render_template("edit_profile.html")

@main_bp.route("/predict", methods=["POST"])
@rate_limit()
def predict():
    """Endpoint para predicción de noticias"""
    try:
        # Obtener datos del formulario
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        model_choice = request.form.get("model", "svm")
        
        # Validar entrada
        if not title or not description:
            return jsonify({
                "success": False,
                "error": "Título y descripción son requeridos"
            }), 400
        
        # Validar límites de caracteres
        is_valid, error_msg = validate_input_length(title, description)
        if not is_valid:
            return jsonify({
                "success": False,
                "error": error_msg
            }), 400
        
        # Verificar permisos de modelo
        if not current_user.is_authenticated and model_choice == "sabert":
            return jsonify({
                "success": False,
                "error": "Debes iniciar sesión para usar el modelo SaBERT"
            }), 403
        
        # Combinar título y descripción
        texto = f"{title}. {description}"
        
        # Realizar predicciones según el modelo seleccionado
        resultados = []
        prediccion_final = None
        confianza_final = 0.0
        
        if not ml_predictor:
            return jsonify({
                "success": False,
                "error": "Modelos de ML no disponibles"
            }), 500
        
        if model_choice == "svm" or model_choice == "both":
            try:
                pred_svm, confianza_svm = ml_predictor.predict_svm(texto)
                etiqueta_svm = "Verdadera" if pred_svm == 1 else "Falsa"
                
                resultados.append({
                    "modelo": "SVM",
                    "prediccion": etiqueta_svm,
                    "confianza": round(confianza_svm, 1),
                    "es_verdadera": pred_svm == 1
                })
                
                if prediccion_final is None:
                    prediccion_final = pred_svm
                    confianza_final = confianza_svm
                    
            except Exception as e:
                resultados.append({
                    "modelo": "SVM",
                    "prediccion": "Error",
                    "confianza": 0.0,
                    "es_verdadera": False
                })
        
        if model_choice == "nb" or model_choice == "both":
            try:
                pred_nb, confianza_nb = ml_predictor.predict_nb(texto)
                etiqueta_nb = "Verdadera" if pred_nb == 1 else "Falsa"
                
                resultados.append({
                    "modelo": "Naive Bayes",
                    "prediccion": etiqueta_nb,
                    "confianza": round(confianza_nb, 1),
                    "es_verdadera": pred_nb == 1
                })
                
                # Si es el único modelo o tiene mayor confianza, usar como final
                if prediccion_final is None or confianza_nb > confianza_final:
                    prediccion_final = pred_nb
                    confianza_final = confianza_nb
                    
            except Exception as e:
                resultados.append({
                    "modelo": "Naive Bayes",
                    "prediccion": "Error",
                    "confianza": 0.0,
                    "es_verdadera": False
                })

        if model_choice == "sabert" and current_user.is_authenticated:
            try:
                pred_sabert, confianza_sabert = ml_predictor.predict_sabert(texto)
                etiqueta_sabert = "Verdadera" if pred_sabert == 1 else "Falsa"

                resultados.append({
                    "modelo": "SaBERT",
                    "prediccion": etiqueta_sabert,
                    "confianza": round(confianza_sabert, 1),
                    "es_verdadera": pred_sabert == 1
                })

                prediccion_final = pred_sabert
                confianza_final = confianza_sabert
                
            except Exception as e:
                resultados.append({
                    "modelo": "SaBERT",
                    "prediccion": "Error",
                    "confianza": 0.0,
                    "es_verdadera": False
                })
        
        # Preparar respuesta
        if model_choice == "both" and len(resultados) == 2:
            # Consenso entre modelos
            consenso = all(r["es_verdadera"] for r in resultados)
            if consenso or not any(r["es_verdadera"] for r in resultados):
                # Ambos coinciden
                confianza_final = sum(r["confianza"] for r in resultados) / len(resultados)
            else:
                # Discrepancia - reducir confianza
                confianza_final = max(r["confianza"] for r in resultados) * 0.7
        
        # Guardar análisis en la base de datos si el usuario está autenticado
        if current_user.is_authenticated:
            try:
                analysis = Analysis(
                    user_id=current_user.id,
                    title=title,
                    description=description,
                    model_used=model_choice,
                    prediction="Verdadera" if prediccion_final == 1 else "Falsa",
                    confidence=confianza_final,
                    is_true=prediccion_final == 1
                )
                db.session.add(analysis)
                db.session.commit()
            except Exception as e:
                print(f"Error guardando análisis: {e}")
                db.session.rollback()
        
        return jsonify({
            "success": True,
            "prediccion_final": "Verdadera" if prediccion_final == 1 else "Falsa",
            "es_verdadera": prediccion_final == 1,
            "confianza": round(confianza_final, 1),
            "modelo_usado": model_choice,
            "resultados_detalle": resultados,
            "texto_analizado": f"{texto[:50]}..." if len(texto) > 50 else texto
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error interno del servidor: {str(e)}"
        }), 500

@main_bp.route("/api/health")
def health_check():
    """Endpoint para verificar que la API está funcionando"""
    return jsonify({
        "status": "OK",
        "message": "FactCheck AI API está funcionando correctamente",
        "models_loaded": {
            "svm": ml_predictor.svm_modelo is not None if ml_predictor else False,
            "naive_bayes": ml_predictor.nb_modelo is not None if ml_predictor else False,
            "vectorizer": ml_predictor.vectorizer is not None if ml_predictor else False,
            "sabert": ml_predictor.modelo_sabert is not None if ml_predictor else False
        }
    })

@main_bp.route("/api/stats")
def get_stats():
    """Endpoint para obtener estadísticas generales"""
    try:
        total_users = User.query.count()
        total_analyses = Analysis.query.count()
        true_analyses = Analysis.query.filter_by(is_true=True).count()
        false_analyses = Analysis.query.filter_by(is_true=False).count()
        
        return jsonify({
            "success": True,
            "stats": {
                "total_users": total_users,
                "total_analyses": total_analyses,
                "true_analyses": true_analyses,
                "false_analyses": false_analyses,
                "accuracy_rate": round((true_analyses / total_analyses * 100) if total_analyses > 0 else 0, 1)
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500 