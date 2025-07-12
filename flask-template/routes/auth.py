from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.database import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        # Validaciones
        if not all([username, email, password, confirm_password]):
            flash("Todos los campos son requeridos", "error")
            return render_template("register.html")
        
        if password != confirm_password:
            flash("Las contraseñas no coinciden", "error")
            return render_template("register.html")
        
        if len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres", "error")
            return render_template("register.html")
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(username=username).first():
            flash("El nombre de usuario ya está en uso", "error")
            return render_template("register.html")
        
        if User.query.filter_by(email=email).first():
            flash("El email ya está registrado", "error")
            return render_template("register.html")
        
        # Crear nuevo usuario
        user = User(username=username, email=email)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash("Cuenta creada exitosamente. Por favor inicia sesión.", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            db.session.rollback()
            flash("Error al crear la cuenta. Por favor intenta de nuevo.", "error")
            return render_template("register.html")
    
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            flash("Usuario y contraseña son requeridos", "error")
            return render_template("login.html")
        
        # Buscar usuario por username o email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f"¡Bienvenido, {user.username}!", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Usuario o contraseña incorrectos", "error")
            return render_template("login.html")
    
    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión exitosamente", "success")
    return redirect(url_for("main.home")) 