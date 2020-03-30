import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret'
    # DB_HOST = '127.0.0.1'
    # DB_USER = 'foobar'
    # DB_PASSWD = 'foobar'
    # DB_DATABASE = 'foobar'
    DB_FILE = './data/database.sqlite'
    ITEMS_PER_PAGE = 10
    JWT_AUTH_URL_RULE = '/api/auth'
    UPLOAD_FOLDER = './tmp'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    PRODUCTION = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
