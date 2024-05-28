import click
from flask import Flask
from flask.cli import FlaskGroup
from src import create_app, db

app = create_app()
cli = FlaskGroup(create_app=lambda: app)

@cli.command('recreate_db')
def recreate_db():
    """Drops and recreates the database."""
    db.drop_all()
    db.create_all()
    db.session.commit()
    click.echo("Database recreated!")

@cli.command('seed_users_sessions_sessionreviews')
def seed_users_sessions_sessionreviews():
    """Seeds the database with Users, Sessions, and SessionReviews and their works."""
    
    
    click.echo("Database seeded with initial users, sessions, and session_reviews.")

if __name__ == "__main__":
    cli()
    app.run(threaded=True)

