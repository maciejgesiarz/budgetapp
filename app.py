import os
from flask import Flask
from config import DevelopmentConfig, ProductionConfig
from extensions import db, migrate, login_manager, oauth
from core import models 

# ... import blueprintów ...

def create_app():
    app = Flask(__name__)

    # wybór configu
    env = os.getenv('FLASK_ENV', 'development')
    cfg = DevelopmentConfig if env == 'development' else ProductionConfig
    app.config.from_object(cfg)

    # inicjalizacja rozszerzeń
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    oauth.init_app(app)


    # rejestracja blueprintów
    app.register_blueprint(transactions_bp)
    app.register_blueprint(settings_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
