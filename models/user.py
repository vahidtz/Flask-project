from db import db
import sqlite3

class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password ):
        self.username = username
        self.password = password
# These two methods acting like an interconnection between the database and the objects in Python.
#SQL JWT only deals with
# objects. Any user should be an object. These methods creates an object if the the realavnat username and pasword
#exits in the data base and return to the python code. So they are very important.
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()


    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
