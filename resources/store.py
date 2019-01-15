from flask_restful import reqparse, Resource
from flask_jwt import jwt_required
from models.item import ItemModel
from models.store import StoreModel


class StoreResource(Resource):


    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        else:
            return {"message": "No such store found."}, 404

    def post (self, name):
        if StoreModel.find_by_name(name):
            return {"mesage":"An item with name '{}' already exists".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message":"An error occured inserting the record."}, 500
        return store.json(), 201


    def delete (self, name):
        store = StoreModel.find_by_name(name)
        if store is None:
            return {"mesage":"A store with name '{}' does not exist".format(name)}, 404
        store.delete_from_db()
        return {"message":"store was deleted"}


class StorelistResource(Resource):
    def get(self):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all() ))}
        # return({'items': [item.json() for item in ItemModel.query.all()]})
