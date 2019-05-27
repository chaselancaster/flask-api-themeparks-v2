from flask import jsonify, Blueprint, abort
from flask_restful import (Resource, Api, reqparse, fields,
                           marshal, marshal_with, url_for)

import models

# defining the fields we want on the responses
trip_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'park': fields.String,
    'date': fields.DateTime
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

    def get(self):
        return jsonify({'trips': [{'name': 'Disneyland'}]})

    def post(self):
        # reading the args aka "req.body"
        args = self.reqparse.parse_args()
        print(args, '<--- args (req.body)')
        # **args turns the inputs from the form into string variables that can be passed to the create function
        trip = models.Trip.create(**args)
        return jsonify({'trips': [{'name': 'Universal Studios'}]})


class Trip(Resource):
    # show route
    def get(self, id):
        return jsonify({'name': 'Disneyland'})

    # update route
    def put(self, id):
        return jsonify({'name': 'Disneyland'})

    # delete route
    def delete(self, id):
        return jsonify({'name': 'Disneyland'})


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
