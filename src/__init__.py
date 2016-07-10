from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "tournament"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t1"

db = MongoEngine(app)

import tournament_test
