from flask import jsonify, Blueprint, abort
from flask_restful import (Resource, Api, reqparse, fields,
                           marshal, marshal_with, url_for)
from flask_login import login_required, current_user
import models

# defining the fields we want on the responses
trip_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'park': fields.String,
    # 'date': fields.DateTime
}


class TripsList(Resource):
    def __init__(self):
        # setting up reqparse
        self.reqparse = reqparse.RequestParser()
        # requiring each to be true so that the user must input these
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No name inputted',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'park',
            required=True,
            help='No park selected',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'date',
            required=False,
            help='No date inputted',
            location=['form', 'json']
        )
        # Inheriting from Resource and calling its init method
        # allows us to use self :)
        super(TripsList, self).__init__()

    # to select all the trips -> models.Trip.select() -> look up peewee queries
    # for generating response object -> look up marshal in flask
    # get route
    def get(self):
        new_trips = [marshal(trip, trip_fields)
                     for trip in models.Trip.select()]
        return new_trips
    # marshal is converting the model into a json object
    @marshal_with(trip_fields)
    def post(self):
        # reading the args aka "req.body"
        args = self.reqparse.parse_args()
        print(args, '<--- args (req.body)')
        # **args turns the inputs from the form into string variables that can be passed to the create function
        trip = models.Trip.create(**args)
        print(trip, '<---', type(trip))
        return (trip, 201)


class Trip(Resource):
    def __init__(self):
        # setting up reqparse
        self.reqparse = reqparse.RequestParser()
        # requiring each to be true so that the user must input these
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No name inputted',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'park',
            required=True,
            help='No park selected',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'date',
            required=False,
            help='No date inputted',
            location=['form', 'json']
        )
        # Inheriting from Resource and calling its init method
        # allows us to use self :)
        super().__init__()

     # show route
    @marshal_with(trip_fields)
    def get(self, id):
        try:
            trip = models.Trip.get(models.Trip.id == id)
        except models.Trip.DoesNotExist:
            abort(404)
        else:
            return(trip, 200)

    # update route
    @marshal_with(trip_fields)
    def put(self, id):
        # parsing args (get req.body)
        args = self.reqparse.parse_args()
        # searching for the Trip that has the same model as we put in
        query = models.Trip.update(**args).where(models.Trip.id == id)
        # executing query
        query.execute()
        print(query, '<--- this is the query')
        # the query doesn't respond with the updated object
        return (models.Trip.get(models.Trip.id == id), 200)

    # delete route
    # you have to execute the update and delete queries
    def delete(self, id):
        query = models.Trip.delete().where(models.Trip.id == id)
        query.execute()
        return {"message": "trip deleted"}


# setting up module of view functions that can be attached to the flask app
trips_api = Blueprint('resources.trips', __name__)
# instantiating the api from the blueprint
api = Api(trips_api)

api.add_resource(
    TripsList,
    '/trips'
)
api.add_resource(
    # Identifying the Trip class above
    Trip,
    # this variable will be passed into the functions above
    '/trips/<int:id>'
)
