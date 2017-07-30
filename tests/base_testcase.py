import unittest
from passlib.hash import bcrypt

from app import app, db
from app.models import User, Bucketlist


class BaseTest(unittest.TestCase):
    def setUp(self):
        #setup test environment configuration
        app.config['SECRET_KEY'] = '8h87yhggfd45dfds22as'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'\
            'localhost/db_for_api_tests'
        self.client = app.test_client()
        db.drop_all()
        db.create_all()

        self.headers = {"Content-Type": "application/json"}
        #define a user to be used for registration tests
        self.temp_user = {
            "username": "Sansa",
            "email": "sansa@gmail.com",
            "password": "wicked",
            "confirm_password": "wicked"
        }

        #define an existing user
        self.saved_user = User("tyrion", "tyrion@gmail.com",
                               bcrypt.hash("lion", rounds=12))
        db.session.add(self.saved_user)
        db.session.commit()        

    def tearDown(self):
        db.session.remove
        db.drop_all()
