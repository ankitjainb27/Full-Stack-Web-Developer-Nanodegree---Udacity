from flask import Flask
from flask.ext.mongoengine import MongoEngine
import os

templates_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'templates/static')

app = Flask(__name__, instance_relative_config=True, template_folder=templates_dir, static_folder=static_dir)
app.config["MONGODB_SETTINGS"] = {'DB': "restaurant"}
app.config["SECRET_KEY"] = "KeepThisS3cr3trestaurant"

db = MongoEngine(app)


def register_blueprints(app):
    from src.api import restaurants
    from src.api import menu
    app.register_blueprint(restaurants)
    app.register_blueprint(menu)


register_blueprints(app)

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.run()

# import lotsofmenus
