import datetime

# Giving model ability to talk to postgres sql
from peewee import *
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

import config

DATABASE = SqliteDatabase('themeparks.sqlite')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE


class Trip(Model):
    name = CharField()
    park = CharField()
    date = DateField()
    # rides = CharField()
    # food = CharField()

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()  # opening connection
    # this array is taking the model and creates tables that match them
    DATABASE.create_tables([Trip], safe=True)
    DATABASE.close()
