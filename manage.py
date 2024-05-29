import click
from flask.cli import FlaskGroup
from src import create_app, db
from src.api.users.models import User
from src.api.appointments.models import Appointment, AppointmentReview
from datetime import datetime

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
    """Seeds the database with Users, Sessions, and SessionReviews."""
    
    user1 = User(name="Alice Johnson", phone_number="123-456-7890", role="student")
    user2 = User(name="Bob Smith", phone_number="098-765-4321", role="coach")
    user3 = User(name="Charlie Brown", phone_number="555-555-5555", role="student")
    user4 = User(name="David Wilson", phone_number="444-444-4444", role="coach")

    db.session.add_all([user1, user2, user3, user4])
    db.session.commit()

    appointment1 = Appointment(coach_id=user2.id, start_time=datetime(2023, 5, 10, 10, 0), student_id=user1.id)
    appointment2 = Appointment(coach_id=user2.id, start_time=datetime(2023, 5, 11, 12, 0))
    appointment3 = Appointment(coach_id=user4.id, start_time=datetime(2023, 5, 12, 14, 0), student_id=user3.id)
    appointment4 = Appointment(coach_id=user4.id, start_time=datetime(2023, 5, 13, 16, 0))

    db.session.add_all([appointment1, appointment2, appointment3, appointment4])
    db.session.commit()

    review1 = AppointmentReview(appointment_id=appointment1.id, satisfaction_score=5, notes="Excellent session!")
    review2 = AppointmentReview(appointment_id=appointment3.id, satisfaction_score=4, notes="Good session with some improvements needed.")

    db.session.add_all([review1, review2])
    db.session.commit()

    click.echo("Database seeded with initial users, sessions, and session reviews.")

if __name__ == "__main__":
    cli()
    app.run(threaded=True)
