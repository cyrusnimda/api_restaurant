
class BaseConfig(object):
    SECRET_KEY='Please_change_this_secret_key_398473723'
    SQLALCHEMY_DATABASE_URI='mysql://username:password@server/db'
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
