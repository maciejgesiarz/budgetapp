import os                                # <-- dodaj ten import
from flask import Flask
from config import DevelopmentConfig, ProductionConfig
from extensions import close_db
from features.transactions.routes import transactions_bp
from features.settings.routes import settings_bp

def create_app():
    app = Flask(__name__)

    # wybierz konfigurację na podstawie FLASK_ENV
    env = os.getenv('FLASK_ENV', 'development')
    cfg = DevelopmentConfig if env == 'development' else ProductionConfig
    app.config.from_object(cfg)

    # teardown DB
    app.teardown_appcontext(close_db)

    # rejestracja blueprintów
    app.register_blueprint(transactions_bp)
    app.register_blueprint(settings_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
