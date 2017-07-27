from app import db

class User(db.Model):
    '''
    Defines properties for a user to generate users table in db
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    bucketlists = db.relationship('Bucketlist', backref='user', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id


class Bucketlist(db.Model):
    '''
    Defines properties for a bucketlist, used to create bucketlists table
    '''
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship(
        'Item', backref='bucketlist', lazy='dynamic')

    def __init__(self, name, description, owner_id):
        self.name = name
        self.description = description
        self.owner_id = owner_id

    def __str__(self):
        return self.name


class Item(db.Model):
    '''
    Defines properties for a bucketlist item, used to create items table
    '''
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(200))
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def __init__(self, title, description, bucket_id):
        self.title = title
        self.description = description
        self.bucket_id = bucket_id

    def __str__(self):
        return self.title

