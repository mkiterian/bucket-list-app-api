from app import app, db
from app.models import User, Bucketlist, Item
from flask_sqlalchemy import SQLAlchemy
import unittest
import json


class UserTest(unittest.TestCase):
    def setUp(self):
        app.config['SECRET_KEY'] = '8h87yhggfd45dfds22as'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/db_for_api_tests'
        self.client = app.test_client()
        db.drop_all()
        db.create_all()

        self.headers = {"Content-Type": "application/json"}
        self.temp_user = {
            "username": "Sansa",
            "email": "sansa@gmail.com",
            "password": "wicked",
            "confirm_password": "wicked"
        }

        self.saved_user = User("tyrion", "tyrion@gmail.com", "lion")
        db.session.add(self.saved_user)
        db.session.commit()
 
    def tearDown(self):
        db.session.remove

    def test_login_returns_ok_status_code(self):
        user = {
            "username": self.saved_user.username,
            "password": self.saved_user.password
        }
        response = self.client.post('/api/v1/auth/login', data=json.dumps(user), headers=self.headers)
        self.assertTrue(response.status_code == 200)

    