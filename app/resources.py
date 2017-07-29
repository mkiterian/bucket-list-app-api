from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import Api, Resource, abort, reqparse
from app import app, db
from .models import Bucketlist, Item, User

api = Api(app, prefix='/api/v1')

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

class UserResource(Resource):
    '''
    Defines handlers for get, post and put user requests
    '''
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, location='json')
        parser.add_argument('email', type=str, required=True, location='json')
        parser.add_argument('password', type=str, required=True, location='json')
        parser.add_argument('confirm_password', type=str, required=True, location='json')

        args = parser.parse_args(strict=True)
        if args['password'] == args['confirm_password']:
            user = User(args['username'], args['email'], args['password'])
            db.session.add(user)
            db.session.commit()
            return {'message': 'user successfully registered!'}

api.add_resource(UserResource, '/auth/register')