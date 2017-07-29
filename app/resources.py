from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import Api, Resource, abort, reqparse
from app import app, db
from .models import Bucketlist, Item, User

api = Api(app)

def verify(username, password):
    if not (username and password):
        return False
    else:
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                return user
        else:
            return False


def identity(payload):
    user_id = payload['identity']
    return {"user_id": user_id}


jwt = JWT(app, verify, identity)