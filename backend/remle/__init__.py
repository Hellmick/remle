from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///remle.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})

from remle import routes
