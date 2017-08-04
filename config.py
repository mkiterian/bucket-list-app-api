class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SECRET_KEY = 'asdfh87sf454yhggfd45dererfds22as112'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/bcktlst'
    JWT_AUTH_URL_RULE = '/api/v1/auth/login'

class TestingConfig(Config):
    SECRET_KEY = '8h87yhggfd45dfds22as'
    TESTING = True
    WTF_CSRF_ENABLED = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://'\
        'localhost/db_for_api_tests'

