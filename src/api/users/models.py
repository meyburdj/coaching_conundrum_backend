from src import db


class User(db.Model):
    __tablename__="users"
    
    id = db.Column(
        db.Integer, 
        primary_key=True
    )
    
    name = db.Column(
        db.String(), 
        nullable=False
    )

    phone_number = db.Column(
        db.String(),
        nullable=False
        )
    
    role = db.Column(
        db.String(10), 
        nullable=False)

    coached_appointments = db.relationship('Appointment', foreign_keys='Appointment.coach_id', backref='coach')
    student_appointments = db.relationship('Appointment', foreign_keys='Appointment.student_id', backref='student')
    
    def __init__(self, name, phone_number, role):
        self.name=name
        self.phone_number=phone_number
        self.role=role