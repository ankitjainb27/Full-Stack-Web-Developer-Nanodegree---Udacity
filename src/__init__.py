from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "tournament"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t1"

db = MongoEngine(app)

# tournament.add()
# print tournament.deletePlayers()
# print tournament.registerPlayer("Chandra Nalaar5")
# tournament.swissPairings()
import tournament_test
