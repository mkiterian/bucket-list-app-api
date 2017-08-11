import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    SECRET_KEY = os.getenv('KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_AUTH_URL_RULE = '/api/v1/auth/login'


class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    SECRET_KEY = '8h87yhggfd45dfds22as'
    TESTING = True
    WTF_CSRF_ENABLED = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://'\
        'localhost/db_for_api_tests'

