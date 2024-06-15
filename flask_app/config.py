from pathlib import Path

basedir = Path(__file__).parent.parent

class BaseConfig:
    SECRET_KEY = "secret key"
    WTF_CSRF_SECRET_KEY = "secret key"

class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATION = False
    SQLALCHEMY_ECHO = True

class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATION = False
    WTF_CSRF_ENABLED = False

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATION = False
    SQLALCHEMY_ECHO = False
    DEBUG = False

config = {
    "testing": TestingConfig,
    "local": LocalConfig,
    "production": ProductionConfig,
}
