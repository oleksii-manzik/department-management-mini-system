import os


class Config:
    DEBUG = False
    SERVER_NAME = 'localhost:5000'
    MYSQL_USER = 'manager_user'
    MYSQL_PASSWORD = 'hard_password1234'
    MYSQL_HOST = 'localhost'
    DB_NAME = 'company_db'
    SQLALCHEMY_DATABASE_URI = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}' \
                              f'@{MYSQL_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = False


class TestConfig(Config):
    DB_NAME = 'test_company_db'
    SQLALCHEMY_DATABASE_URI = f'mysql://{Config.MYSQL_USER}:' \
                              f'{Config.MYSQL_PASSWORD}' \
                              f'@{Config.MYSQL_HOST}/{DB_NAME}'


def run_config():
    env = os.environ.get('ENV')
    if env == 'DEV':
        return DevConfig
    elif env == 'TEST':
        return TestConfig
    return Config
