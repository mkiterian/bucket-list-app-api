from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)

from . import models
from . import resources