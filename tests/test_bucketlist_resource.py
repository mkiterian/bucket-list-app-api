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

        self.response = self.client.post(
            '/api/v1/auth/login', data=json.dumps(self.user),
            headers=self.headers)
        self.response_content = json.loads(self.response.data)
        self.headers['Authorization'] = 'JWT {}'.format(
            self.response_content['access_token'])

    def tearDown(self):
        super(BucketlistResourceTest, self).tearDown()

    # view bucketlists tests
    def test_view_bucketlists_status_code_is_ok(self):
        response = self.client.get(
            '/api/v1/bucketlists', data=json.dumps(self.user),
            headers=self.headers)
        self.assertEqual(response.status_code, 200)
    
    def test_if_bucketlist_name_is_returned(self):
        response = self.client.get(
            '/api/v1/bucketlists', data=json.dumps(self.user),
            headers=self.headers)
        self.assertTrue(b'bucketlist_one' in response.data)

    def test_all_bucketlists_are_returned(self):
        response = self.client.get(
            '/api/v1/bucketlists', data=json.dumps(self.user),
            headers=self.headers)
        self.assertTrue(b'bucketlist_one' in response.data
                        and b'bucketlist_two' in response.data)

    def test_cant_view_bucketlists_without_token(self):
        no_token = self.headers
        no_token['Authorization'] = ""
        response = self.client.get(
            '/api/v1/bucketlists', data=json.dumps(self.user),
            headers=no_token)
        self.assertTrue(b'Authorization Required' in response.data)

    #view specific bucketlist
    def test_successful_status_code_when_bucket_id_is_specified(self):
        response = self.client.get(
            '/api/v1/bucketlists/{}'.format(self.bucketlist_one_id),
            data=json.dumps(self.user),
            headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_bucketlist_name_is_returned_given_id(self):
        response = self.client.get(
            '/api/v1/bucketlists/{}'.format(self.bucketlist_one_id),
            data=json.dumps(self.user),
            headers=self.headers)

        self.assertTrue(b'bucketlist_one' in response.data)

    def test_only_one_bucketlist_is_returned_given_id(self):
        response = self.client.get(
            '/api/v1/bucketlists/{}'.format(self.bucketlist_one_id),
            data=json.dumps(self.user),
            headers=self.headers)

        self.assertEqual(response.data.count(b'id'), 1)

    def test_response_message_for_non_existent_id(self):
        response = self.client.get(
            '/api/v1/bucketlists/2000',
            data=json.dumps(self.user),
            headers=self.headers)
        self.assertTrue(b'requested id does not exist' in response.data)

    # create bucketlist tests
    def test_bucketlist_created_successfully_message(self):
        new_bucketlist = {
            "name": "new bucketlist",
            "description": "this is a test bucketlist"
        }
        response = self.client.post(
            '/api/v1/bucketlists',
            data=json.dumps(new_bucketlist),
            headers=self.headers)
        self.assertTrue(response.status_code, 201)
        self.assertTrue(b'bucketlist created successfully' in response.data)

    def test_create_bucketlist_request_missing_field_message(self):
        new_bucketlist = {
            "name": "new bucketlist"
        }
        response = self.client.post(
            '/api/v1/bucketlists',
            data=json.dumps(new_bucketlist),
            headers=self.headers)
        self.assertTrue(b'Missing required parameter' in response.data)

    def test_create_bucketlist_request_with_empty_strings(self):
        new_bucketlist = {
            "name": "",
            "description": "this has no name"
        }
        response = self.client.post(
            '/api/v1/bucketlists',
            data=json.dumps(new_bucketlist),
            headers=self.headers)
        self.assertTrue(b'empty strings not allowed' in response.data)

    def test_cant_create_bucketlist_without_authentication(self):
        new_bucketlist = {
            "name": "Not allowed",
            "description": "I have not been authenticated!"
        }
        no_token = self.headers
        no_token['Authorization'] = ""
        response = self.client.post(
            '/api/v1/bucketlists',
            data=json.dumps(new_bucketlist),
            headers=no_token)
        self.assertTrue(b'Authorization Required' in response.data)

    # Update bucketlists tests
    def test_bucketlist_successfully_updated_message(self):
        updates = {
            "name": "the first one",
            "description": "there will be another"
        }
        response = self.client.put(
            '/api/v1/bucketlists/{}'.format(
                self.example_bucketlist_one.id),
            data=json.dumps(updates),
            headers=self.headers)
        self.assertTrue(b'bucketlist updated successfully'
                        in response.data)

    def test_message_bucketlist_id_does_not_exist(self):
        updates = {
            "name": "the first one",
            "description": "there will be another"
        }
        response = self.client.put(
            '/api/v1/bucketlists/{}'.format(89),
            data=json.dumps(updates),
            headers=self.headers)
        self.assertTrue(b'does not exist' in response.data)

    def test_update_bucketlist_request_with_empty_strings(self):
        updates = {
            "name": "",
            "description": "this has no name"
        }
        response = self.client.put(
            '/api/v1/bucketlists/{}'.format(
                self.example_bucketlist_one.id),
            data=json.dumps(updates),
            headers=self.headers)
        self.assertTrue(b'empty strings not allowed' in response.data)

    # delete bucketlist tests
    def test_bucketlist_deleted_successfully_message(self):
        response = self.client.delete(
            '/api/v1/bucketlists/{}'.format(
                self.example_bucketlist_one.id),
            data={},
            headers=self.headers)
        self.assertTrue(b'bucketlist deleted successfully'
                        in response.data)

    def test_message_for_invalid_bucketlist_id(self):
        response = self.client.delete(
            '/api/v1/bucketlists/{}'.format(21), data={},
            headers=self.headers)
        self.assertTrue(response.status_code == 404)
        self.assertTrue(
            b'cannot delete non-existent bucketlist' in response.data)
    