from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import prefs

db = SQLAlchemy()

def create_flask_app():
    app = Flask(__name__, template_folder='/home/t/ingroup/templates/', static_folder='/home/t/ingroup/static')
    app.config.from_object(prefs.Config)
    db.init_app(app)
    return app