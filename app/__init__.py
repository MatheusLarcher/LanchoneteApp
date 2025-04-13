# app/__init__.py
from flask import Flask
from app.models import db
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar SQLAlchemy com o app
    db.init_app(app)
    
    # Registrar blueprints
    from app.routes import init_routes
    init_routes(app)
    
    # Template filters
    from app.utils.helpers import format_currency
    app.jinja_env.filters['format_currency'] = format_currency
    
    return app