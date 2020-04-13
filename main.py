import os

from app import create_app
from app import db


app_config = os.environ.get('APP_CONFIG')
app = create_app(app_config)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db)


@app.cli.command()
def createdb():
    db.create_all()


