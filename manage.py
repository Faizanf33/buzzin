from flask.cli import FlaskGroup

from project import create_app, db
from project.models import (
    User,
    Role
)

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
    """Recreates a local database."""
    print("Recreating database...")
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def create_db():
    """Creates a local database."""
    print("Creating database...")
    db.create_all()
    db.session.commit()


@cli.command()
def seed_db():
    """Seeds the database."""
    print("Seeding database...")

    User(
        firstname="Admin",
        lastname="User",
        email="admin@processpioneering.com",
        password="greaterthaneight",
        role=Role.ADMIN
    ).save()

    print("Database seeded!")


if __name__ == "__main__":
    cli()
