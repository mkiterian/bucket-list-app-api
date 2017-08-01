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
        if bucketlist:
            if len(args['name'].strip()) == 0 or len(
                    args['description'].strip()) == 0:
                return {'message': 'empty strings not allowed'}
            else:
                bucketlist.name = args['name']
                bucketlist.description = args['description']

                db.session.merge(bucketlist)
                db.session.commit()
                return {'message': 'bucketlist updated successfully'}
        else:
            return {'message': 'does not exist'}

    @jwt_required()
    def delete(self, id):
        bucketlist = Bucketlist.query.get(id)
        if bucketlist is not None:
            db.session.delete(bucketlist)
            db.session.commit()
            return {'message': 'bucketlist deleted successfully'}
        else:
            return {'message': 'cannot delete non-existent bucketlist'}


class ItemResource(Resource):
    '''
    handles get, post, put and delete item requests
    '''
    @jwt_required()
    def get(self, id, item_id=None):
        bucketlist = Bucketlist.query.get(id)
        print(bucketlist)
        if bucketlist is not None:
            if item_id is not None:
                item = Item.query.filter_by(bucket_id=id,
                                            id=item_id).first()
                if item:
                    return {'id': item.id,
                            'title': item.title,
                            'description': item.description}
                else:
                    return {'message': 'item does not exist'}
            else:
                result = Item.query.filter_by(bucket_id=id).all()

                items = dict()
                for item in result:
                    items[item.id] = {'title': item.title,
                                    'description': item.description}
                return items
        else:
            return {'message': 'bucketlist does not exist'}

    @jwt_required()
    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, location='json')
        parser.add_argument('description', type=str, required=True, location='json')

        args = parser.parse_args(strict=True)
        if len(args['title'].strip()) == 0 or len(
                    args['description'].strip()) == 0:
                return {'message': 'empty strings not allowed'}
        else:
            new_item = Item(args['title'], args['description'], id)
            db.session.add(new_item)
            db.session.commit()
            return {'message': 'item created successfully'}

    @jwt_required()
    def put(self, id, item_id):        
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, location='json')
        parser.add_argument('description', type=str, required=True, location='json')

        args = parser.parse_args(strict=True)

        item = Item.query.filter_by(id=item_id, bucket_id=id).first()
        if item:
            if len(args['title'].strip()) == 0 or len(
                    args['description'].strip()) == 0:
                return {'message': 'empty strings not allowed'}
            else:
                item.title = args['title']
                item.description = args['description']
        else:
            return {'message': 'item does not exist'}

        db.session.merge(item)
        db.session.commit()
        return {'message': 'item updated successfully'}

    @jwt_required()
    def delete(self, id, item_id):
        item = Item.query.filter_by(id=item_id, bucket_id=id).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            return {'message': 'item deleted successfully'}
        else: 
            return {'message': 'cannot delete, item does not exist'}
        


api.add_resource(UserResource, '/auth/register')
api.add_resource(BucketlistResource,
                 '/bucketlists/<int:id>', '/bucketlists')
api.add_resource(ItemResource,
                 '/bucketlists/<int:id>/items/<item_id>',
                 '/bucketlists/<int:id>/items')
