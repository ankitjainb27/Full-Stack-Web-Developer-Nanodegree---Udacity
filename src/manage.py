import os, sys

print sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server
from src import app

manager = Manager(app)

manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=False,
    host='0.0.0.0',
    port=5000))

if __name__ == "__main__":
    manager.run()


