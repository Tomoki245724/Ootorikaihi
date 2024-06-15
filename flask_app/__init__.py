from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_httpauth import HTTPBasicAuth

from flask_app.config import config

db = SQLAlchemy()

csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.login_view = "main.signup"
login_manager.login_message = ""

auth = HTTPBasicAuth()

users = {
    "user": "password",
}

@auth.get_password
def get_pw(username):
    return users.get(username) if username in users else None

def create_app(config_key):
    app = Flask(__name__)

    app.config.from_object(config[config_key])

    csrf.init_app(app)

    db.init_app(app)
    Migrate(app, db)

    login_manager.init_app(app)

    from flask_app.views import main as main_bp
    app.register_blueprint(main_bp, url_prefix="/")

    return app
