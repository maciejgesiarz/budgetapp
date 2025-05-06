# app.py

import os
from flask import Flask
from flask_migrate import Migrate

from config import DevelopmentConfig, ProductionConfig
from extensions import db, login_manager, oauth

# Blueprinty
from features.auth import auth_bp
from features.transactions.routes import transactions_bp
from features.categories.routes import categories_bp
# (w przyszłości)
# from features.analysis.routes   import analysis_bp

def create_app():
    app = Flask(__name__)

    # 1. Konfiguracja
    env = os.getenv('FLASK_ENV', 'development')
    cfg = ProductionConfig if env == 'production' else DevelopmentConfig
    app.config.from_object(cfg)

    # 2. Inicjalizacja rozszerzeń
    db.init_app(app)
    Migrate(app, db)  # możesz też importować migrate z extensions jeśli wolisz
    login_manager.init_app(app)
    oauth.init_app(app)

    # 3. Rejestracja blueprintów
    app.register_blueprint(auth_bp)                    # /settings/auth/...
    app.register_blueprint(transactions_bp, url_prefix='/transactions')
    app.register_blueprint(categories_bp,   url_prefix='/categories')
    # app.register_blueprint(analysis_bp,     url_prefix='/analysis')

    return app

# Wskazówka CLI Flask: ustaw zmienną FLASK_APP=app:create_app
