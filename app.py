from flask import Flask, after_this_request
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
app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET")

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="None",
)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except:
        return None


CORS(
    posts,
    origins=["http://localhost:3000", "https://gamers-on-record.up.railway.app"],
    supports_credentials=True,
)  # heroku url goes after local for all
CORS(
    user,
    origins=["http://localhost:3000", "https://gamers-on-record.up.railway.app"],
    supports_credentials=True,
)
CORS(
    games,
    origins=["http://localhost:3000", "https://gamers-on-record.up.railway.app"],
    supports_credentials=True,
)

app.register_blueprint(posts, url_prefix="/posts")
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(games, url_prefix="/games")


@app.before_request
def before_request():

    """Connect to the db before each request"""
    print("you should see this before each request")
    models.DATABASE.connect()

    @after_this_request
    def after_request(response):
        """Close the db connetion after each request"""
        print("you should see this after each request")
        models.DATABASE.close()
        return response


# if os.environ.get("FLASK_ENV") != "development":
#     print("\non heroku!")
#     models.initialize()

if __name__ == "__main__":
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
