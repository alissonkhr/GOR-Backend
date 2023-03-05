from peewee import *
import datetime, os
from flask_login import UserMixin

# import os
from playhouse.db_url import connect

# if "ON_HEROKU" in os.environ:
#     DATABASE = connect(os.environ.get("DATABASE_URL"))
# else:
# DATABASE = SqliteDatabase("gor.sqlite")
DATABASE = connect(os.environ.get('DATABASE_URL') or 'sqlite:///gor.sqlite')
# Connect to the database URL defined in the environment, falling
# back to a local Sqlite database if no database URL is specified.



class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE


class UserPost(Model):
    game = CharField()
    message = CharField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(User, backref="my_posts")

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()


DATABASE.create_tables([User, UserPost], safe=True)
print("Connected to DB, tables created if not already existing")
DATABASE.close()
