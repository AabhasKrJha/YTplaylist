class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = b'\x1b\xe1eTh\x8f:\xd5\xfaB\xdb\x85qC\xb0>\x03\xa3H\xbb.\x02\xd3 \x13\xacwJ\x87(Z\xce'
    ENV = "development"
    FLASK_ENV = "development"
    # SQLALCHEMY_DATABASE_URI = "sqlite:///users.db"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    ENV = "production"
    FLASK_ENV = "production"
    
class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///users_test.db"
