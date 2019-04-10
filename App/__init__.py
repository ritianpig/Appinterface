from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask("App")
app.config.from_pyfile('config.py')
app.config['JSON_AS_ASCII'] = False


db = SQLAlchemy(app)
migrate = Migrate(app)
migrate.init_app(app, db)

from . import api
import models