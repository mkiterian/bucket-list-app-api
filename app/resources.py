from passlib.hash import bcrypt

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
            if bcrypt.verify(password, user.password):
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
        parser.add_argument('username', type=str,
                            required=True, location='json')
        parser.add_argument('email', type=str, required=True,
                            location='json')
        parser.add_argument('password', type=str,
                            required=True, location='json')
        parser.add_argument('confirm_password', type=str,
                            required=True, location='json')

        args = parser.parse_args(strict=True)
        if args['username']:
            if args['email']:
                if args['password'] == args['confirm_password']:
                    hash = bcrypt.hash(args['password'], rounds=12)
                    user = User(args['username'],
                                args['email'], hash)
                    db.session.add(user)
                    db.session.commit()
                    return {'message': 'user successfully registered!'}
                else:
                    return {'message': 'Make password should match '
                                       'confirm password'}
            else:
                return {'message': 'email is required'}
        else:
            return {'message': 'username is required'}


class BucketlistResource(Resource):
    '''
    Defines handlers for get, post and put bucketlist requests
    '''
    @jwt_required()
    def get(self, id=None):
        if id is not None:
            bucketlist = Bucketlist.query.get(id)
            if bucketlist is not None:
                return {
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'description': bucketlist.description
                }
            else:
                return {'message': 'requested id does not exist'}
        else:
            result = Bucketlist.query.all()

            bucketlists = dict()
            for bucketlist in result:
                bucketlists[bucketlist.id] = {
                    'name': bucketlist.name,
                    'description': bucketlist.description
                }
            return bucketlists

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name',
                            type=str, required=True, location='json')
        parser.add_argument('description', type=str,
                            required=True, location='json')

        args = parser.parse_args(strict=True)
        if len(args['name'].strip()) == 0 or len(
            args['description'].strip()) == 0:
            return {'message': 'empty strings not allowed'}
        else:
            new_bucketlist = Bucketlist(
                args['name'], args['description'],
                current_identity['user_id'])
            db.session.add(new_bucketlist)
            db.session.commit()
            return {'message': 'bucketlist created successfully'}

    @jwt_required()
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name',
                            type=str, required=True, location='json')
        parser.add_argument('description', type=str,
                            required=True, location='json')

        args = parser.parse_args(strict=True)

        bucketlist = Bucketlist.query.filter_by(id=id).first()
        bucketlist.name = args['name']
        bucketlist.description = args['description']

        db.session.merge(bucketlist)
        db.session.commit()
        return {'message': 'bucketlist updated successfully'}


api.add_resource(UserResource, '/auth/register')
api.add_resource(BucketlistResource,
                 '/bucketlists/<int:id>', '/bucketlists')
