import click
from flask.cli import with_appcontext
from app import db

@click.group()
def cli():
    pass

@click.command()
@with_appcontext
def init_db():
    db.create_all()
    click.echo('Initialized the database.')

@click.command()
@with_appcontext
def create_superuser():
    # Add logic to create a superuser
    pass

@click.command()
@with_appcontext
def seed_demo():
    # Add logic to seed the database with demo data
    pass

cli.add_command(init_db)
cli.add_command(create_superuser)
cli.add_command(seed_demo)

if __name__ == '__main__':
    cli()
