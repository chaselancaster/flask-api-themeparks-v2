import datetime

# Giving model ability to talk to postgres sql
from peewee import *
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin, current_user, login_required


DATABASE = SqliteDatabase('amusementpark.sqlite')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, verify_password, **kwargs):
        email = email.lower()
        try:
            cls.select().where(
                (cls.email == email)
            ).get()
        except cls.DoesNotExist:
            user = cls(username=username, email=email)
            user.password = generate_password_hash(password)

            user.save()
            return user
        else:
            raise Exception('User with that email already exists')


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
    DATABASE.create_tables([Trip, User], safe=True)
    DATABASE.close()
