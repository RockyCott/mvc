import os

# config class for app.config
class Config:
    SECRET_KEY = 'secret'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    SESSION_COOKIE_SECURE = True
    #SESSION_COOKIE_HTTPONLY = True
    #SESSION_COOKIE_SAMESITE='Lax'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USERNAME = 
    # MAIL_PASSWORD = 
    # MAIL_DEFAULT_SENDER = 
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024 # file upload limit to 3Mb

