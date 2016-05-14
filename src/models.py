import datetime
from flask import url_for
from src import db


class Match(db.Document):
    winner = db.StringField(max_length=255, required=True)
    loser = db.StringField(max_length=255, required=True)


class Player(db.Document):
    name = db.StringField(max_length=255, required=True)

    def __unicode__(self):
        return str(self.id) + self.name

    meta = {
        'allow_inheritance': False
    }
