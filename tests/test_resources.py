from flask_sqlalchemy import SQLAlchemy
import unittest
import json
from passlib.hash import bcrypt

from app import app, db
from app.models import User, Bucketlist, Item


class UserTest(unittest.TestCase):
    def setUp(self):
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
        self.temp_user = {
            "username": "Sansa",
            "email": "sansa@gmail.com",
            "password": "wicked",
            "confirm_password": "wicked"
        }

        self.saved_user = User("tyrion", "tyrion@gmail.com",
                               bcrypt.hash("lion", rounds=12))
        db.session.add(self.saved_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove
        db.drop_all()

    def test_login_returns_ok_status_code(self):
        user = {
            "username": self.saved_user.username,
            "password": "lion"
        }
        response = self.client.post(
            '/api/v1/auth/login', data=json.dumps(user),
            headers=self.headers)
        self.assertTrue(response.status_code == 200)

    def test_login_success_response_has_token(self):
        user = {
            "username": self.saved_user.username,
            "password": "lion"
        }
        response = self.client.post(
            '/api/v1/auth/login', data=json.dumps(user),
            headers=self.headers)
        self.assertTrue(b'access_token' in response.data)

    def test_wrong_login_credentials_returns_correct_message(self):
        user = {
            "username": "john",
            "password": "dorian"
        }
        response = self.client.post(
            '/api/v1/auth/login', data=json.dumps(user),
            headers=self.headers)
        self.assertTrue(b'Invalid credentials' in response.data)

    def test_empty_submit_returns_correct_message(self):
        user = {
            "username": "",
            "password": ""
        }
        response = self.client.post(
            '/api/v1/auth/login', data=json.dumps(user),
            headers=self.headers)
        self.assertTrue(b'Invalid credentials' in response.data)

    def test_register_returns_ok_status_code(self):
        user = self.temp_user
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(user),
            headers=self.headers)
        self.assertTrue(response.status_code == 200)

    def test_succesful_register_contains_success_message(self):
        user = self.temp_user
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(user),
            headers=self.headers)
        self.assertTrue(b'user successfully registered!'
                        in response.data)

    def test_register_missing_username_message(self):
        user = self.temp_user
        user['username'] = ''
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(user),
            headers=self.headers)
        self.assertTrue(b'username is required' in response.data)

    def test_register_missing_email_message(self):
        user = self.temp_user
        user['email'] = ''
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(user),
            headers=self.headers)
        self.assertTrue(b'email is required' in response.data)


    def test_register_password_doesnt_match_confirm_message(self):
        user = self.temp_user
        user['confirm_password'] = 'wrong'
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(user),
            headers=self.headers)
        self.assertTrue(b'Make password should match '
                        b'confirm password' in response.data)
