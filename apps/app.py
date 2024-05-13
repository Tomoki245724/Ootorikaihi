from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from apps.config import config

db = SQLAlchemy()

csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.login_view = "auth.signup"
login_manager.login_message = ""

def create_app(config_key):
    app = Flask(__name__)

    app.config.from_object(config[config_key])

    csrf.init_app(app)

    db.init_app(app)
    Migrate(app, db)

    login_manager.init_app(app)

    from apps.crud import views as crud_views
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    from apps.auth import views as auth_views
    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    from apps.maps import views as maps_views
    # url_prefix="/maps"としないほうが良いと思うが、その場合の静的ファイルの指定方法が不明
    app.register_blueprint(maps_views.maps, url_prefix="/maps")

    return app
