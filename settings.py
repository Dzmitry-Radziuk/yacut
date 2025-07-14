import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER_NAME = os.getenv("SERVER_NAME", "localhost:5000")
