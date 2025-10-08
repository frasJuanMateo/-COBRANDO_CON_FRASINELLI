from flask import Flask, render_template
from flask_cors import CORS
from flask_login import LoginManager
from py.db import db
from py.db import Usuario
from py.rutas import rutas

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:461315@localhost/tienda_online'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave_super_secreta'

db.init_app(app)
app.register_blueprint(rutas)

login_manager = LoginManager(app)
login_manager.login_view = 'rutas.login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
def main():
    return render_template('main.html')

if __name__ == "__main__":
    app.run(debug=True)