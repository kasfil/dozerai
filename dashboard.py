from flask import Flask

from webapp import home
from webapp.api import images

app = Flask(__name__)


app.register_blueprint(home.bp)
app.register_blueprint(images.bp)
