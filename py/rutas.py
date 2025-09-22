from flask import Blueprint, request, jsonify
from py.db import db   
import base64
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import random
import string


apis = Blueprint("apis", __name__)