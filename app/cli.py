import os
from dataclasses import dataclass

import click
from sqlalchemy_utils import create_database, database_exists, drop_database


@dataclass
class Database:
    url: str = None
    name: str = None

database = Database()


def register(app):
    @app.cli.group()
    def manage_db():
        '''Commands that manage the database'''
        database.url = app.config.get("SQLALCHEMY_DATABASE_URI")
        database.name = database.url.split('/')[-1]
    
    @manage_db.command()
    def create_db():
        '''This command create a database with given db name'''
        if database_exists(database.url):
            click.secho(f'database [{database.name}] already exists', fg='yellow', bold=True)
        else:
            create_database(database.url)
            click.secho(f'database [{database.name}] created', fg='green', bold=True)

    @manage_db.command()
    def destroy_db():
        '''This command destroy a database with given db name'''
        if database_exists(database.url):
            drop_database(database.url)
            click.secho(f'database {database.name} destroyed', fg='green', bold=True)
        else:
            click.secho(f'database {database.name} does not exists', fg='yellow', bold=True)
    
    @manage_db.command()
    def create_all():
        '''This command will create all tables and relations'''
        # print(dir(app))
        db = app.extensions.get('sqlalchemy').db
        # print(dir(db))
        db.create_all()
        # app_context = app.app_context()
        # app_context.push()
        # db = app.extensions.get('sqlalchemy').db
        # db.create_all()

    @manage_db.command()
    def reset_db():
        '''This command will delete and create database and tables'''
        if database_exists(database.url):
            click.secho(f'deleting {database.name} database...', fg='yellow', bold=True)
            try:
                drop_database(database.url)
            except Exception as e:
                print(e.args)
            click.secho(f'database {database.name} destroyed', fg='green', bold=True)

            click.secho(f'creating {database.name} database', fg='yellow', bold=True)
            try:
                create_database(database.url)
            except Exception as e:
                print(e.args)
            click.secho(f'database {database.name} created', fg='green', bold=True)
        else:
            click.secho(f'creating {database.name} database', fg='yellow', bold=True)
            try:
                create_database(database.url)
            except Exception as e:
                print(e.args)
            click.secho(f'database {database.name} created', fg='green', bold=True)
    
        
        # db = app.extensions.get('sqlalchemy').db
        # db.create_all()

    @manage_db.command()
    @click.argument('name', default='root')
    def create_admin(name):
        '''This command will create a super user'''
        print(name)
        #TODO: criar lógica para adicionar um usuário admin na aplicação
    



