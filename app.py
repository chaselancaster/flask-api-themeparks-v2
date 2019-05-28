import config
from flask import Flask, g
import models

from resources.users import users_api  # importing blueprint
from resources.trips import trips_api
from flask_cors import CORS
from flask_login import LoginManager
# setting up login
login_manager = LoginManager()


app = Flask(__name__)
app.secret_key = config.SECRET_KEY
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


CORS(trips_api, origins=["http://localhost:3000"], supports_credentials=True)
CORS(users_api, origins=["http://localhost:3000"], supports_credentials=True)
# every route will start with /api/v1 in the blueprint
# setting blueprint up to be used
app.register_blueprint(trips_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/api/v1')


@app.before_request
def before_request():
    '''Connect to the database before each request'''
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    '''Close the database connection after each request'''
    g.db.close()
    return response

# default route

# below is the function that the client requests
# then function after is what happens after that request
# to define method @app.route('/', method = "Post")
@app.route('/')  # decorator
def index():
    return "testing testing"


# this is saying when we run python app.py, this is the main file
if __name__ == '__main__':
    # starting the server
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)
