from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask("APP")
app.config.from_pyfile('config.py')


db = SQLAlchemy(app)
migrate = Migrate(app)
migrate.init_app(app, db)

from . import api
import models