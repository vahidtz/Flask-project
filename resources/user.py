## User class is defined in this file
## UserResource is defined in this file, coming with an end point
from flask_restful import Resource, reqparse
import sqlite3
from models.user import UserModel


class UserResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
    type = str,
    required = True,
    help = 'This field cannot be left blank')

    parser.add_argument('password',
    type = str,
    required = True,
    help = 'This field cannot be left blank')

    def post(self):
        request_data = UserResource.parser.parse_args()
        if UserModel.find_by_username(request_data['username']):
            return {"mesage":"A username with name '{}' already exists".format(request_data['username'])}, 400

        user = UserModel(**request_data)

        try:
            user.save_to_db()
            return {"Message":"A username was created."}, 201
        except:
            return {"message":"An error occured inserting the record."}, 500
