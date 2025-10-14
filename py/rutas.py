from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from py.db import db
from py.db import Usuario, Producto
from py.forms import RegistroForm, LoginForm

rutas = Blueprint('rutas', __name__)

@rutas.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistroForm()
    if form.validate_on_submit():
        nuevo = Usuario(nombre=form.nombre.data, email=form.email.data)
        nuevo.set_password(form.password.data)
        db.session.add(nuevo)
        db.session.commit()
        flash('Registro exitoso, ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('rutas.login'))
    return render_template('register.html', form=form)

@rutas.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('rutas.dashboard'))
        else:
            flash('Email o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form)

@rutas.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('rutas.login'))

@rutas.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@rutas.route('/')
def main():
    productos = Producto.query.all()
    return render_template('main.html', productos=productos)