import os
from flask import Flask

from config import DevelopmentConfig, ProductionConfig
from extensions import db, migrate, login_manager, oauth
from core.models import User

# Blueprinty
from features.auth import auth_bp
from features.transactions.routes import transactions_bp
from features.categories.routes import categories_bp


def create_app():
    app = Flask(__name__)

    # 1. Konfiguracja
    env = os.getenv('FLASK_ENV', 'development')
    cfg = ProductionConfig if env == 'production' else DevelopmentConfig
    app.config.from_object(cfg)

    # 2. Inicjalizacja rozszerzeń
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    # Ustawienie strony logowania
    login_manager.login_view = 'auth.login'
    # Loader użytkownika dla Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    oauth.init_app(app)

    # Rejestracja klienta Google OAuth2
    oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

    # 3. Rejestracja blueprintów
    app.register_blueprint(auth_bp)                    # /settings/auth/...
    app.register_blueprint(transactions_bp, url_prefix='/transactions')
    app.register_blueprint(categories_bp,   url_prefix='/categories')
    # app.register_blueprint(analysis_bp,     url_prefix='/analysis')

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
