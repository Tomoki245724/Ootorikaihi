from flask_app import create_app
from flask_app.config import config

app = create_app(config_key="local")

if __name__ == '__main__':
    app.run()
