from flask import Flask, render_template,Blueprint, request, jsonify, redirect, url_for
from flask_cors import CORS
from jinja2 import TemplateNotFound
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

rutas = Blueprint('rutas', __name__,template_folder='templates')