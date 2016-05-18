from flask.ext.classy import FlaskView, route
from flask import request, Response
import json



form = """
<form action = "/home/">
    <input name = "q">
    <input type = "submit">
<form>
"""

class HomeConfigView(FlaskView):
    def get(self):
        return form


class HomeView(FlaskView):
    def get(self):
        print "asda"
        params = request.args
        query = params.get('q','').strip()
        return query
