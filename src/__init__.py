from main import app
from .api import HomeView, HomeConfigView



HomeView.register(app)
HomeConfigView.register(app)
