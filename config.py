import os

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'zmień-to-bezpiecznym')
    DATABASE   = os.path.join(os.getcwd(), 'transactions.db')

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False
