from flask import Flask
from .routes import api_blueprint
from .models import init_db
from config import Config
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    # 启用 CORS

    app.config.from_object(Config)
    init_db(app)
    app.register_blueprint(api_blueprint, url_prefix='/api')
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
    return app
