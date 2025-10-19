from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired, MultipleFileField

class RegistroForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirmar = PasswordField('Confirmar contraseña', validators=[
        DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir')
    ])
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')
    
class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del producto', validators=[DataRequired(), Length(min=3, max=100)])
    descripcion = TextAreaField('Descripción', validators=[Length(max=500)])
    precio = DecimalField('Precio', validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    imagenes = MultipleFileField('Imágenes del producto', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Solo se permiten imágenes.')
    ])
    submit = SubmitField('Publicar producto')