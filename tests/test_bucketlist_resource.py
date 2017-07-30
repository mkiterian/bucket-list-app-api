from flask_sqlalchemy import SQLAlchemy
import unittest
import json
from passlib.hash import bcrypt

from app import app, db
from app.models import User, Bucketlist
from base_testcase import BaseTest


class BucketlistResourceTest(BaseTest):
    def setUp(self):
        super(BucketlistResourceTest, self).setUp()

    def tearDown(self):
        super(BucketlistResourceTest, self).tearDown()

    def test_view_bucketlists_status_code_is_ok(self):
        user = {
            "username": self.saved_user.username,
            "password": "lion"
        }
        response = self.client.post(
            '/api/v1/auth/login', data=json.dumps(user),
            headers=self.headers)
        response_content = json.loads(response.data)
        #print(response_content['access_token'])
        self.headers['Authorization'] = 'JWT {}'.format(response_content['access_token'])
        print('JWT {}'.format(self.headers))
        response = self.client.post(
            '/api/v1/bucketlists', data=json.dumps(user),
            headers=self.headers)
        self.assertEqual(response.status_code, 200)
