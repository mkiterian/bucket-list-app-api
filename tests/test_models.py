from unittest import TestCase
from app import app, db
from app.models import User, Bucketlist, Item

class UserTestCase(TestCase):
    
    def setUp(self):
        app.config['SECRET_KEY'] = '8h87yhggfd45dfds22as'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/db_for_api_tests'
        db.drop_all()
        db.create_all()
        self.user = User('homer', 'homer@gmail.com', 'secret')

    def tearDown(self):
        db.session.remove()

    def test_user_successfully_added_to_db(self):
        db.session.add(self.user)
        db.session.commit
        user  = User.query.filter_by(username='homer').first()
        self.assertTrue(self.user.id)

    def test_user_has_bucketlist_property(self):
        self.assertTrue(hasattr(self.user, 'bucketlists'))


class BucketlistTestCase(TestCase):
    def setUp(self):
        self.bucketlist = Bucketlist('Vacationing', 'Go places', 100)

    def test_bucketlist_has_item_property(self):
        self.assertTrue(hasattr(self.bucketlist, 'items'))

class ItemTestCase(TestCase):
    def setUp(self):
        self.item = Item('Go to Egypt', 'It\'s a pyramid scheme', 100)
        print(self.item)

    def test_item_has_been_created(self):
        self.assertEqual(str(self.item), 'Go to Egypt')