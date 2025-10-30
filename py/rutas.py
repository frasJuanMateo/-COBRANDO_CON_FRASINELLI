from flask import Blueprint, render_template, redirect, url_for, flash, send_file, make_response, request
from flask_login import login_user, logout_user, login_required, current_user
from py.db import db
from py.db import Usuario, Producto, Imagen, Carrito
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
        # Crear el producto
        producto = Producto(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            precio=form.precio.data,
            stock=form.stock.data,
            usuario_id=current_user.id
        )
        db.session.add(producto)
        db.session.commit()

        # Guardar cada imagen subida
        if form.imagenes.data:
            for archivo in form.imagenes.data:
                if archivo and archivo.filename != '':
                    nombre_seguro = secure_filename(archivo.filename)
                    datos_bytes = archivo.read()  # leer contenido binario
                    nueva_img = Imagen(
                        nombre_archivo=nombre_seguro,
                        datos=datos_bytes,
                        producto_id=producto.id
                    )
                    db.session.add(nueva_img)
            db.session.commit()

        flash('Producto creado exitosamente con sus imágenes.', 'success')
        return redirect(url_for('rutas.dashboard'))

    return render_template('nuevo_producto.html', form=form)

@rutas.route('/producto/<int:producto_id>')
def producto(producto_id):
    en_carrito = False
    producto = Producto.query.get_or_404(producto_id)
    items = Carrito.query.filter_by(usuario_id=current_user.id).all()
    
    if producto.id in [item.producto_id for item in items]:
        en_carrito = True
    
    return render_template('producto.html', producto=producto, en_carrito=en_carrito)

@rutas.route('/agregar_al_carrito/<int:producto_id>', methods=['POST'])
@login_required
def agregar_al_carrito(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    cantidad = int(request.form.get('cantidad', 1))

    # Validar stock
    if cantidad > producto.stock:
        flash('No hay suficiente stock disponible.', 'danger')
        return redirect(url_for('rutas.producto', producto_id=producto.id))

    nuevo_item = Carrito(
        usuario_id=current_user.id,
        producto_id=producto.id,
        cantidad=cantidad
    )
    db.session.add(nuevo_item)
    db.session.commit()

    flash(f'Se añadió {cantidad} unidad(es) de "{producto.nombre}" al carrito.', 'success')
    return redirect(url_for('rutas.producto', producto_id=producto.id))

@rutas.route('/carrito')
@login_required
def carrito():
    # Traer todos los ítems del carrito del usuario actual
    items = Carrito.query.filter_by(usuario_id=current_user.id).all()
    
    # Calcular el total
    total = sum(item.producto.precio * item.cantidad for item in items)

    return render_template('lista_carrito.html', items=items, total=total)

@rutas.route('/eliminar_del_carrito/<int:item_id>', methods=['POST'])
@login_required
def eliminar_del_carrito(item_id):
    item = Carrito.query.get_or_404(item_id)

    # Solo el usuario dueño del carrito puede eliminarlo
    if item.usuario_id != current_user.id:
        flash("No tienes permiso para eliminar este producto.", "danger")
        return redirect(url_for('rutas.carrito'))

    db.session.delete(item)
    db.session.commit()
    flash("Producto eliminado del carrito.", "success")
    return redirect(url_for('rutas.carrito'))