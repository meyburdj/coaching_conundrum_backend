from flask_restx import Namespace, Resource, fields
from flask import request
from .crud import (
    create_appointment, read_appointment, read_appointments, update_appointment, delete_appointment,
    create_appointment_review, read_appointments_by_coach, read_appointments_by_student
)


appointments_namespace = Namespace('appointments')

appointment_review_model = appointments_namespace.model('AppointmentReview', {
    'id': fields.Integer(readOnly=True),
    'appointment_id': fields.Integer(required=True, description='ID of the appointment'),
    'satisfaction_score': fields.Integer(required=True, description='Satisfaction score (1-5)'),
    'notes': fields.String(required=True, description='Review notes')
})

appointment_model = appointments_namespace.model('Appointment', {
    'id': fields.Integer(readOnly=True),
    'coach_id': fields.Integer(required=True, description='ID of the coach'),
    'coach_name': fields.String(readOnly=True, description='Name of the coach'),
    'start_time': fields.DateTime(required=True, description='Start time of the appointment'),
    'student_id': fields.Integer(description='ID of the student'),
    'review': fields.Nested(appointment_review_model, required=False)
})


class AppointmentResource(Resource):
    @appointments_namespace.marshal_with(appointment_model)
    def get(self, id):
        try:
            appointment = read_appointment(id)
            if appointment:
                return appointment, 200
            else:
                appointments_namespace.abort(404, f"Appointment with id {id} not found")
        except ValueError as e:
            appointments_namespace.abort(500, str(e))

    @appointments_namespace.expect(appointment_model)
    @appointments_namespace.marshal_with(appointment_model)
    def patch(self, id):
        try:
            data = request.get_json()
            student_id = data['student_id']
            appointment = update_appointment(id, student_id)
            return appointment, 200
        except KeyError as e:
            appointments_namespace.abort(400, f"Missing required field: {e}")
        except ValueError as e:
            appointments_namespace.abort(400, str(e))
        except Exception as e:
            appointments_namespace.abort(500, str(e))

    def delete(self, id):
        try:
            delete_appointment(id)
            return '', 204
        except ValueError as e:
            appointments_namespace.abort(400, str(e))
        except Exception as e:
            appointments_namespace.abort(500, str(e))

class AppointmentList(Resource):
    @appointments_namespace.marshal_list_with(appointment_model)
    def get(self):
        try:
            selected_time = request.args.get('selected_time')
            available = request.args.get('available')
            if available is not None:
                available = available.lower() == 'true'
            appointments = read_appointments(selected_time, available)
            # if appointments:
            return appointments, 200
            # else:
            #     appointments_namespace.abort(404, "No appointments found")
        except ValueError as e:
            appointments_namespace.abort(500, str(e))

    @appointments_namespace.expect(appointment_model)
    @appointments_namespace.marshal_with(appointment_model, code=201)
    def post(self):
        try:
            data = request.get_json()
            coach_id = data['coach_id']
            start_time = data['start_time']
            appointment = create_appointment(coach_id=coach_id, start_time=start_time)
            return appointment, 201
        except KeyError as e:
            appointments_namespace.abort(400, f"Missing required field: {e}")
        except ValueError as e:
            appointments_namespace.abort(400, str(e))
        except Exception as e:
            appointments_namespace.abort(500, str(e))

class AppointmentReview(Resource):
    @appointments_namespace.expect(appointment_review_model)
    @appointments_namespace.marshal_with(appointment_review_model, code=201)
    def post(self, id):
        try:
            data = request.get_json()
            satisfaction_score = data['satisfaction_score']
            notes = data['notes']
            review = create_appointment_review(id, satisfaction_score, notes)
            return review, 201
        except KeyError as e:
            appointments_namespace.abort(400, f"Missing required field: {e}")
        except ValueError as e:
            appointments_namespace.abort(400, str(e))
        except Exception as e:
            appointments_namespace.abort(500, str(e))

class CoachAppointments(Resource):
    @appointments_namespace.marshal_list_with(appointment_model)
    def get(self, coach_id):
        try:
            appointments = read_appointments_by_coach(coach_id)
            if appointments:
                return appointments, 200
            else:
                appointments_namespace.abort(404, f"No appointments found for coach with id {coach_id}")
        except ValueError as e:
            appointments_namespace.abort(500, str(e))

class StudentAppointments(Resource):
    @appointments_namespace.marshal_list_with(appointment_model)
    def get(self, student_id):
        try:
            appointments = read_appointments_by_student(student_id)
            if appointments:
                return appointments, 200
            else:
                appointments_namespace.abort(404, f"No appointments found for student with id {student_id}")
        except ValueError as e:
            appointments_namespace.abort(500, str(e))

appointments_namespace.add_resource(AppointmentList, '/')
appointments_namespace.add_resource(AppointmentResource, '/<int:id>')
appointments_namespace.add_resource(CoachAppointments, '/coach/<int:coach_id>')
appointments_namespace.add_resource(StudentAppointments, '/student/<int:student_id>')
appointments_namespace.add_resource(AppointmentReview, '/<int:id>/review')
