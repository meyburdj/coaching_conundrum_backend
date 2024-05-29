from src import db
from sqlalchemy.exc import IntegrityError
from .models import User


def create_user(name, phone_number, role):
    try:
        user = User(name=name, phone_number=phone_number, role=role)
        db.session.add(user)
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error creating user: {e}")

def read_user(user_id):
    try:
        return User.query.filter(User.id == user_id).first()
    except Exception as e:
        raise ValueError(f"Error reading user {user_id}: {e}")

def read_users():
    try:
        return User.query.all()
    except Exception as e:
        raise ValueError(f"Error reading users: {e}")