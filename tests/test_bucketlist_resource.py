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
        self.user = {
            "username": self.saved_user.username,
            "password": "lion"
        }

        # create a bucketlist for tyrion
        current_user = User.query.filter_by(
            username=self.saved_user.username).first()
        self.example_bucketlist_one = Bucketlist(
            "bucketlist_one",
            "this is an example bucketlist",
            current_user.id)
        db.session.add(self.example_bucketlist_one)
        db.session.commit()

        # create a second bucketlist for tyrion
        self.example_bucketlist_two = Bucketlist(
            "bucketlist_two",
            "this is an another bucketlist",
            current_user.id)
        db.session.add(self.example_bucketlist_two)
        db.session.commit()

        self.bucketlist_one_id = Bucketlist.query.filter_by(
            name="bucketlist_one").first().id

    def tearDown(self):
        super(BucketlistResourceTest, self).tearDown()

    def test_view_bucketlists_status_code_is_ok(self):
        response = self.client.post(
            '/api/v1/auth/login', data=json.dumps(self.user),
            headers=self.headers)
        response_content = json.loads(response.data)
        self.headers['Authorization'] = 'JWT {}'.format(
            response_content['access_token'])
        response = self.client.get(
            '/api/v1/bucketlists', data=json.dumps(self.user),
            headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_if_bucketlist_name_is_returned(self):
        response = self.client.post(
            '/api/v1/auth/login', data=json.dumps(self.user),
            headers=self.headers)
        response_content = json.loads(response.data)
        self.headers['Authorization'] = 'JWT {}'.format(
            response_content['access_token'])
        response = self.client.get(
            '/api/v1/bucketlists', data=json.dumps(self.user),
            headers=self.headers)
        self.assertTrue(b'bucketlist_one' in response.data)

    def test_all_bucketlists_are_returned(self):
        response = self.client.post(
            '/api/v1/auth/login', data=json.dumps(self.user),
            headers=self.headers)
        response_content = json.loads(response.data)
        self.headers['Authorization'] = 'JWT {}'.format(
            response_content['access_token'])
        response = self.client.get(
            '/api/v1/bucketlists', data=json.dumps(self.user),
            headers=self.headers)
        self.assertTrue(b'bucketlist_one' in response.data
                        and b'bucketlist_two' in response.data)

    def test_cant_view_bucketlists_without_token(self):
        response = self.client.get(
            '/api/v1/bucketlists', data=json.dumps(self.user),
            headers=self.headers)
        self.assertTrue(b'Authorization Required' in response.data)

    def test_successful_status_code_when_bucket_id_is_specified(self):
        response = self.client.post(
            '/api/v1/auth/login', data=json.dumps(self.user),
            headers=self.headers)
        response_content = json.loads(response.data)
        self.headers['Authorization'] = 'JWT {}'.format(
            response_content['access_token'])
        response = self.client.get(
            '/api/v1/bucketlists/{}'.format(self.bucketlist_one_id),
            data=json.dumps(self.user),
            headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_bucketlist_name_is_returned_given_id(self):
        response = self.client.post(
            '/api/v1/auth/login', data=json.dumps(self.user),
            headers=self.headers)
        response_content = json.loads(response.data)
        self.headers['Authorization'] = 'JWT {}'.format(
            response_content['access_token'])
        response = self.client.get(
            '/api/v1/bucketlists/{}'.format(self.bucketlist_one_id),
            data=json.dumps(self.user),
            headers=self.headers)
        
        self.assertTrue(b'bucketlist_one' in response.data)

    def test_only_one_bucketlist_is_returned_given_id(self):
        response = self.client.post(
            '/api/v1/auth/login', data=json.dumps(self.user),
            headers=self.headers)
        response_content = json.loads(response.data)
        self.headers['Authorization'] = 'JWT {}'.format(
            response_content['access_token'])
        response = self.client.get(
            '/api/v1/bucketlists/{}'.format(self.bucketlist_one_id),
            data=json.dumps(self.user),
            headers=self.headers)
        
        self.assertEqual(response.data.count(b'id'), 1)

    def test_response_message_for_non_existent_id(self):
        response = self.client.post(
            '/api/v1/auth/login', data=json.dumps(self.user),
            headers=self.headers)
        response_content = json.loads(response.data)
        self.headers['Authorization'] = 'JWT {}'.format(
            response_content['access_token'])
        response = self.client.get(
            '/api/v1/bucketlists/2000',
            data=json.dumps(self.user),
            headers=self.headers)
        self.assertTrue(b'requested id does not exist' in response.data)

        
