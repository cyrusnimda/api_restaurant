# copy this file as config.py and edit database info, etc.

class BaseConfig(object):
    SECRET_KEY='Please_change_this_secret_key_398473723'
    SQLALCHEMY_DATABASE_URI='mysql://username:password@server/db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATE_FORMAT = "%Y-%m-%d %H:%M"
    PORT = 8080
    BOOKING_HOURS = [
        '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', 
        '19:00', '19:30', '20:00', '20:30', '21:00', '21:30',
        '22:00'
        ]

class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
