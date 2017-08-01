from flask_sqlalchemy import SQLAlchemy
import unittest
import json
from passlib.hash import bcrypt

from app import app, db
from app.models import User, Bucketlist, Item
from base_testcase import BaseTest


class ItemResourceTest(BaseTest):
    def setUp(self):
        super(ItemResourceTest, self).setUp()
        self.user = {
            "username": self.saved_user.username,
            "password": "lion"
        }

        # create a bucketlist for tyrion
        current_user = User.query.filter_by(
            username=self.saved_user.username).first()
        self.example_bucketlist_one = Bucketlist(
            "bucketlist with items",
            "this is bucketlist has items",
            current_user.id)
        db.session.add(self.example_bucketlist_one)
        db.session.commit()

        self.bucketlist_with_items_id = Bucketlist.query.filter_by(
            name="bucketlist with items").first().id

        self.item_1 = Item('Item one', 'this is item one',
                           self.bucketlist_with_items_id)
        self.item_2 = Item('Item two', 'this is item two',
                           self.bucketlist_with_items_id)
        db.session.add(self.item_1)
        db.session.add(self.item_2)
        db.session.commit()

        self.response = self.client.post(
            '/api/v1/auth/login', data=json.dumps(self.user),
            headers=self.headers)
        self.response_content = json.loads(self.response.data)
        self.headers['Authorization'] = 'JWT {}'.format(
            self.response_content['access_token'])

    def tearDown(self):
        super(ItemResourceTest, self).tearDown()

    def test_item_names_returned_by_view_bucketlists(self):
        response = self.client.get(
            '/api/v1/bucketlists/{}/items'.format(
                self.bucketlist_with_items_id),
            headers=self.headers)
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Item one' in response.data)
        self.assertTrue(b'Item two' in response.data)

    def test_cannot_view_items_without_token(self):
        no_token = self.headers
        no_token['Authorization'] = ""
        response = self.client.get(
            '/api/v1/bucketlists/{}/items'.format(
                self.bucketlist_with_items_id),
            data=json.dumps(self.user),
            headers=no_token)
        self.assertTrue(b'Authorization Required' in response.data)
