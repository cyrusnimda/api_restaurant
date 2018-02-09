import os


# default config
class BaseConfig(object):
    SECRET_KEY='Th1s_is_A_s3cret_k3Y'
    SQLALCHEMY_DATABASE_URI='sqlite:///restaurant.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATE_FORMAT = "%Y-%m-%d %H:%M"


class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
