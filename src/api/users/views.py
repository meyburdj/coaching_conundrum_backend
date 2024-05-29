from flask_restx import Namespace, Resource, fields
from flask import request
from .crud import create_user, read_user, read_users

users_namespace = Namespace('users')

user_model = users_namespace.model('User', {
    'id': fields.Integer(readOnly=True),
    'name': fields.String(required=True, description='Name of the user', example='John Doe'),
    'phone_number': fields.String(required=True, description='Phone number of the user', example='123-456-7890'),
    'role': fields.String(required=True, enum=['student', 'coach'], description='Role of the user')
})

class UserResource(Resource):
    @users_namespace.marshal_with(user_model)
    def get(self, id):
        try:
            user = read_user(id)
            if user:
                return user, 200
            else:
                users_namespace.abort(404, f"User with id {id} not found")
        except ValueError as e:
            users_namespace.abort(500, str(e))

class UserList(Resource):
    @users_namespace.marshal_list_with(user_model)
    def get(self):
        try:
            users = read_users()
            if users:
                return users, 200
            else:
                users_namespace.abort(404, "No users found")
        except ValueError as e:
            users_namespace.abort(500, str(e))

    @users_namespace.expect(user_model)
    @users_namespace.marshal_with(user_model, code=201)
    def post(self):
        try:
            data = request.get_json()
            name = data['name']
            phone_number = data['phone_number']
            role = data['role']

            if role not in ['student', 'coach']:
                users_namespace.abort(400, "Invalid role. Role must be 'student' or 'coach'.")

            user = create_user(name=name, phone_number=phone_number, role=role)
            return user, 201
        except KeyError as e:
            users_namespace.abort(400, f"Missing required field: {e}")        
        except ValueError as e:
            users_namespace.abort(400, str(e))
        except Exception as e:
            users_namespace.abort(500, str(e))

users_namespace.add_resource(UserList, '/')
users_namespace.add_resource(UserResource, '/<int:id>')
