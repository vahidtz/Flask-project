# Restful libraru will be used. no longer you will need to use app.route()
from flask import Flask, jsonify
from flask_restful import Api # reqparse is a package itself, used to control payload coming form client
from flask_jwt import JWT
from security import authenticate, identity as identity_function # These methods gives back the user object that contianes IF,
#username and passsword based on username, passowrd for authenticate and userID for identity.
from resources.user import UserResource
from resources.item import ItemResource, ItemlistResource
from resources.store import StoreResource, StorelistResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Jose'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity_function) # It creats a path as:  /auth
# jwt will have three parametrs: app, authenticate and identity methods.

@jwt.auth_response_handler
def cutomized_response_handlerr(access_token, identity):
    return jsonify ({
    'access_token':
    access_token.decode('utf8'),
    'user_id': identity.id
    })


api.add_resource(ItemResource, '/item/<string:name>') # http://127.0.0.1:5000/item/<name>
api.add_resource(ItemlistResource, '/items') # http://127.0.0.1:5000/items
api.add_resource(UserResource, '/register') # http://127.0.0.1:5000/signup
api.add_resource(StorelistResource, '/stores')
api.add_resource(StoreResource,'/store/<string:name>')
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port = 5000, debug = True)
