from app import create_app
from app import db

app = create_app('development')


@app.cli.command()
def createdb():
    db.create_all()
