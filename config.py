import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    # LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    DB_HOST = os.environ.get("DB_HOST")
    DB_NAME = os.environ.get("DB_NAME")
    DATABASE_URL = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JOBS = [
        {
            'id': 'fetch_rss',
            'func': 'app.jobs.fetcher:context_fetch_rss',
            'trigger': 'interval',
            'seconds': 1800 # 1/2 half hour
        }
    ]
    SCHEDULER_API_ENABLED = True

    @staticmethod
    def init_app():
        pass

    @classmethod
    def make_db_url(cls, db_name: str):
        cls.SQLALCHEMY_DATABASE_URI = f"postgresql://{cls.DB_USER}:{cls.DB_PASS}@{cls.DB_HOST}/{db_name}"


class DevelopmentConfig(Config):
    DEBUG = True

    @staticmethod
    def init_app():
        Config.make_db_url('development')

class TestingConfig(Config):
    TESTING = True

    @staticmethod
    def init_app():
        Config.make_db_url('testing')

class ProductionConfig(Config):
    pass
    
    
class HerokuConfig(ProductionConfig):
    '''Heroku Config'''
    @staticmethod
    def init_app():
        try:
            SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
        except KeyError:
            raise EnvironmentError("MUST SET DATABASE_URL")

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'heroku': HerokuConfig,
    'default': DevelopmentConfig
}

