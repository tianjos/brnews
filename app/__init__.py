import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
from config import config, Config


app = Flask(__name__)
db = SQLAlchemy()
scheduler = APScheduler()
migrate = Migrate(app, db)

def create_app(config_name=None) -> Flask:
    # app = Flask(__name__)
    cfg = config.get(config_name)
    cfg.init_app()
    app.config.from_object(cfg) if cfg else app.config.from_object('default')
    db.init_app(app)
    migrate.init_app(app, db)
    # with app.app_context():
    #     db.create_all()

    scheduler.init_app(app)
    scheduler.start()

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app

# def create_all(db: SQLAlchemy, app: Flask) -> None:
#     with app.app_context:
#         db.create_all()
    

from app import models
