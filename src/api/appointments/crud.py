from src import db
from sqlalchemy.exc import IntegrityError
from .models import Appointment, AppointmentReview
from datetime import datetime
from src.api.users.models import User
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy.orm import aliased


def create_appointment(coach_id, start_time):
    try:
        #TODO: Add check to make sure time slot is available
        appointment = Appointment(coach_id=coach_id, start_time=start_time)
        db.session.add(appointment)
        db.session.commit()
        return appointment
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error creating appointment: {e}")

def read_appointment(appointment_id):
    try:
        return Appointment.query.filter(Appointment.id == appointment_id).first()
    except Exception as e:
        raise ValueError(f"Error reading appointment {appointment_id}: {e}")

def read_appointments(selected_time=None, available=None):
    try:
        query = db.session.query(
            Appointment.id,
            Appointment.coach_id,
            User.name.label('coach_name'),
            Appointment.start_time,
            Appointment.student_id
        ).join(User, User.id == Appointment.coach_id).order_by(Appointment.start_time)

        if selected_time:
            try:
                selected_date = datetime.strptime(selected_time, '%Y-%m-%d')
                year = selected_date.year
                month = selected_date.month
                query = query.filter(db.extract('year', Appointment.start_time) == year,
                                     db.extract('month', Appointment.start_time) == month)
            except ValueError:
                raise ValueError("Invalid date format for selected_time. Expected format: YYYY-MM-DD")

        if available is not None:
            if available:
                query = query.filter(and_(Appointment.student_id.is_(None), Appointment.start_time > datetime.now()))
            else:
                query = query.filter(Appointment.student_id.isnot(None))

        return query.all()
    except Exception as e:
        raise ValueError(f"Error reading appointments: {e}")

def update_appointment(appointment_id, student_id):
    try:
        appointment = Appointment.query.filter(Appointment.id == appointment_id).first()
        if appointment:
            if appointment.student_id is not None:
                raise ValueError("Appointment is already booked.")

            appointment.student_id = student_id
            db.session.commit()
            updated_appointment = db.session.query(
                Appointment.id,
                Appointment.coach_id,
                User.name.label('coach_name'),
                User.phone_number,
                Appointment.start_time,
                Appointment.student_id
            ).join(User, User.id == Appointment.coach_id).filter(Appointment.id == appointment_id).first()

            return updated_appointment
            # return appointment
        else:
            raise ValueError(f"Appointment with id {appointment_id} not found.")
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error updating appointment {appointment_id}: {e}")

def delete_appointment(appointment_id):
    try:
        appointment = Appointment.query.filter(Appointment.id == appointment_id).first()
        if appointment:
            db.session.delete(appointment)
            db.session.commit()
        else:
            raise ValueError(f"Appointment with id {appointment_id} not found.")
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error deleting appointment {appointment_id}: {e}")

def create_appointment_review(appointment_id, satisfaction_score, notes):
    try:
        review = AppointmentReview(appointment_id=appointment_id, satisfaction_score=satisfaction_score, notes=notes)
        db.session.add(review)
        db.session.commit()
        return review
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error creating appointment review: {e}")

def read_appointments_by_coach(coach_id):
    try:
        Coach = aliased(User)
        Student = aliased(User)
        
        appointments = db.session.query(
            Appointment.id.label('id'),
            Appointment.coach_id.label('coach_id'),
            Coach.name.label('coach_name'),
            Coach.phone_number.label('phone_number'),
            Appointment.start_time.label('start_time'),
            Appointment.student_id.label('student_id'),
            Student.name.label('student_name'),
            func.coalesce(
                func.json_build_object(
                    'id', AppointmentReview.id,
                    'appointment_id', AppointmentReview.appointment_id,
                    'satisfaction_score', AppointmentReview.satisfaction_score,
                    'notes', AppointmentReview.notes
                ),
                func.json_build_object(
                    'id', None,
                    'appointment_id', None,
                    'satisfaction_score', None,
                    'notes', None
                )
            ).label('review')
        ).outerjoin(
            AppointmentReview, Appointment.id == AppointmentReview.appointment_id
        ).outerjoin(
            Coach, Coach.id == Appointment.coach_id
        ).outerjoin(
            Student, Student.id == Appointment.student_id
        ).filter(
            Appointment.coach_id == coach_id
        ).all()

        result = [
            {
                'id': appointment.id,
                'coach_id': appointment.coach_id,
                'coach_name': appointment.coach_name,
                'phone_number': appointment.phone_number,
                'start_time': appointment.start_time,
                'student_id': appointment.student_id,
                'student_name': appointment.student_name,
                'review': appointment.review
            }
            for appointment in appointments
        ]
        return result
    except Exception as e:
        raise ValueError(f"Error reading appointments for coach {coach_id}: {e}")

def read_appointments_by_student(student_id):
    try:
        return db.session.query(
            Appointment.id,
            Appointment.coach_id,
            User.name.label('coach_name'),
            User.phone_number,
            Appointment.start_time,
            Appointment.student_id
        ).join(User, User.id == Appointment.coach_id).filter(
            and_(Appointment.student_id == student_id, Appointment.start_time > datetime.now())).order_by(Appointment.start_time).all()
    except Exception as e:
        raise ValueError(f"Error reading appointments for student {student_id}: {e}")
