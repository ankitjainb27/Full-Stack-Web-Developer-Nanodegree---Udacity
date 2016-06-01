import datetime
from flask import url_for
from src import db


class MenuItem(db.EmbeddedDocument):
    menu_id = db.SequenceField()
    name = db.StringField(max_length=255, required=True)
    description = db.StringField(max_length=500)
    price = db.StringField(max_length=255)
    course = db.StringField(max_length=255)

    def __unicode__(self):
        return str(self.menu_id) + self.name

    meta = {
        'allow_inheritance': False
    }

    @property
    def serialize(self):
        return {
            'menu_id': self.menu_id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'course': self.course,
        }


class Restaurant(db.Document):
    restaurant_id = db.SequenceField()
    name = db.StringField(max_length=255, required=True)
    menuitems = db.EmbeddedDocumentListField(MenuItem)

    def __unicode__(self):
        return str(self.restaurant_id) + self.name
