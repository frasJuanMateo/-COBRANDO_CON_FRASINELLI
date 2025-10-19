from flask import Blueprint, render_template, redirect, url_for, flash, send_file, make_response
from flask_login import login_user, logout_user, login_required, current_user
from py.db import db
from py.db import Usuario, Producto, Imagen
from werkzeug.utils import secure_filename
from py.forms import RegistroForm, LoginForm, ProductoForm
import io

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
    productos = Producto.query.all()
    return render_template('dashboard.html', productos=productos)

@rutas.route('/')
def main():
    productos = Producto.query.all()
    return render_template('main.html', productos=productos)

@rutas.route('/imagen/<int:imagen_id>')
def mostrar_imagen(imagen_id):
    imagen = Imagen.query.get_or_404(imagen_id)
    # Convertimos los bytes a un stream
    return send_file(
        io.BytesIO(imagen.datos),
        mimetype='image/jpeg',  # o 'image/png' si usás varios tipos
        download_name=imagen.nombre_archivo
    )

@rutas.route('/nuevo_producto', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        # Crear producto
        producto = Producto(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            precio=form.precio.data,
            stock=form.stock.data,
            usuario_id=current_user.id
        )
        db.session.add(producto)
        db.session.commit()

        # Guardar varias imágenes en BLOB
        if form.imagenes.data:
            for archivo in form.imagenes.data:
                if archivo:  # evita errores si algún campo viene vacío
                    nombre_seguro = secure_filename(archivo.filename)
                    datos_bytes = archivo.read()
                    nueva_img = Imagen(
                        nombre_archivo=nombre_seguro,
                        datos=datos_bytes,
                        producto_id=producto.id
                    )
                    db.session.add(nueva_img)
            db.session.commit()

        flash('Producto creado con imágenes correctamente.', 'success')
        return redirect(url_for('rutas.dashboard'))

    return render_template('nuevo_producto.html', form=form)