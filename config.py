import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_AUTH_URL_RULE = '/api/v1/auth/login'

class DevelopmentConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
class TestingConfig(Config):
    SECRET_KEY = '8h87yhggfd45dfds22as'
    TESTING = True
    WTF_CSRF_ENABLED = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://'\
        'localhost/db_for_api_tests'

