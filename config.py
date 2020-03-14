import os
# from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))

# from app.jobs.fetcher import fetch_rss, job1

def job():
    print('job started...')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_TIMEZONE = 'America/Sao_Paulo'
    JOBS = [
        {
            'id': 'fetch_rss',
            # 'func': 'allowed_host:job1',
            'func': 'app.jobs.fetcher:context_fetch_rss',
            'trigger': 'interval',
            'seconds': 60
        }
    ]
    SCHEDULER_API_ENABLED = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
   DEBUG = True
   SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    



config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
