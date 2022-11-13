from flask import Flask
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()

from resources.post import posts
from resources.user import user
from resources.games import games
import models
from flask_cors import CORS

DEBUG = True
PORT = os.environ.get("PORT")
login_manager = LoginManager()
app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET")
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except:
        return None

CORS(posts, origins=["http://localhost:3000"], supports_credentials=True)
CORS(user, origins=["http://localhost:3000"], supports_credentials=True)
CORS(games, origins=["http://localhost:3000"], supports_credentials=True)

app.register_blueprint(posts, url_prefix="/posts")
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(games, url_prefix="/games")

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)