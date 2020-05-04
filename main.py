import os

from app import create_app
from app import db, cli


app_config = os.environ.get('APP_CONFIG')
app = create_app(app_config)
cli.register(app)


# @app.shell_context_processor
# def make_shell_context():
#     return dict(app=app, db=db)


# @app.cli.command()
# def createdb():
#     db.create_all()

# @app.cli.command()
# def deploy():
#     """Run deployment tasks."""
#     db_url = app.config['SQLALCHEMY_DATABASE_URI']
#     if database_exists(db_url):
#         print('Deleting database')
#         drop_database(db_url)
#     else:
#         print('Creating database')
#         create_database(db_url)
