import os


class Config(object):
    """Конфигурация приложения."""

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #Для локальных тестов
    #SERVER_NAME = os.getenv("SERVER_NAME", "localhost:5000")
