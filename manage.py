import click
from flask.cli import with_appcontext
from app import create_app
from app.extensions import db
from app.models import User, Organization

# Ensure app context exists when invoking this script directly
app = create_app()
app.app_context().push()

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
@click.argument('email')
@click.argument('password')
def create_superuser(email, password):
    org = Organization.query.filter_by(slug='jusb-solutions').first()
    if not org:
        org = Organization(name='JusB Solutions', slug='jusb-solutions')
        db.session.add(org)
        db.session.commit()

    user = User(email=email, org_id=org.id, role='jusb_admin')
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo(f'Superuser {email} created.')

@click.command()
@with_appcontext
def seed_demo():
    # Create organizations
    org1 = Organization(name='Acme Corp', slug='acme-corp')
    org2 = Organization(name='Contoso Ltd', slug='contoso-ltd')
    org_jusb = Organization(name='JusB Solutions', slug='jusb-solutions')
    db.session.add_all([org1, org2, org_jusb])
    db.session.commit()

    # Create users
    user1 = User(email='client1@acme.com', org_id=org1.id, role='client')
    user1.set_password('password')
    user2 = User(email='admin@contoso.com', org_id=org2.id, role='client_admin')
    user2.set_password('password')
    jusb_admin = User(email='admin@jusb.com', org_id=org_jusb.id, role='jusb_admin')
    jusb_admin.set_password('password')
    db.session.add_all([user1, user2, jusb_admin])
    db.session.commit()

    click.echo('Demo data seeded.')

cli.add_command(init_db)
cli.add_command(create_superuser)
cli.add_command(seed_demo)

if __name__ == '__main__':
    cli()
