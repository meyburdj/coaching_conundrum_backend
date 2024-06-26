from flask_restx import Api

from src.api.ping import ping_namespace
from src.api.users.views import users_namespace
from src.api.appointments.views import appointments_namespace

api = Api(version="1.0", title="Users API", doc="/doc")

api.add_namespace(ping_namespace, path="/ping")
api.add_namespace(users_namespace, path="/users")
api.add_namespace(appointments_namespace, path="/appointments")
