from flask import Flask, g
import models

from resources.trips import trips_api  # importing blueprint

DEBUG = True
PORT = 8000

app = Flask(__name__)

# every route will start with /api/v1 in the blueprint
app.register_blueprint(trips_api, url_prefix='/api/v1')


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
    app.run(debug=DEBUG, port=PORT)
