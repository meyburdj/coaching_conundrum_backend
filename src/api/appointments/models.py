from src import db

class Appointment(db.Model):
    __tablename__ = "appointments"
    
    id = db.Column(
        db.Integer, 
        primary_key=True
        )
    
    coach_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'), 
        nullable=False
        )
    
    start_time = db.Column(
        db.DateTime, 
        nullable=False
        )
    
    student_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'), 
        nullable=True)

    def __init__(self, coach_id, start_time, student_id=None):
        self.coach_id = coach_id
        self.start_time = start_time
        self.student_id = student_id

class AppointmentReview(db.Model):
    __tablename__ = "appointment_reviews"
    
    id = db.Column(
        db.Integer, 
        primary_key=True
        )
    
    appointment_id = db.Column(
        db.Integer, 
        db.ForeignKey('appointments.id'), 
        nullable=False
        )
    
    satisfaction_score = db.Column(
        db.Integer, 
        nullable=False
        )
    
    notes = db.Column(
        db.Text, 
        nullable=False
        )

    def __init__(self, appointment_id, satisfaction_score, notes):
        self.appointment_id = appointment_id
        self.satisfaction_score = satisfaction_score
        self.notes = notes