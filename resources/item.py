
from flask_restful import reqparse, Resource
from flask_jwt import jwt_required
from models.item import ItemModel


class ItemResource(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('price',
    type = float,
    required = True,
    help = 'price cannot be left blank')
    #request_data = request.get_json() # This line was repalced with abobve lines to have more control on
    #coming data

    parser.add_argument('store_id',
    type = int,
    required = True,
    help = 'ُstore_id cannot be left blank')

    @jwt_required()
    def get(self, name):
        row = ItemModel.find_by_name(name)
        if row:
            return row.json(), 200
        else:
            return {"message": "No such item found."}, 404

    def post (self, name):
        if ItemModel.find_by_name(name):
            return {"mesage":"An item with name '{}' already exists".format(name)}, 400

        request_data = ItemResource.parser.parse_args()
        item = ItemModel(name, request_data['price'], request_data['store_id'] )
        try:
            item.save_to_db()
        except:
            return {"message":"An error occured inserting the record."}, 500
        return item.json(), 201

    def put(self, name):
        request_data = ItemResource.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **request_data)
        else:
            item.price = request_data['price']
            item.store_id = request_data['store_id']

        try:
            item.save_to_db()
        except:
            return {"message":"An error occured updating/inserting the record."}, 500

        return item.json()

    def delete (self, name):
        item = ItemModel.find_by_name(name)
        if item is None:
            return {"mesage":"An item with name '{}' does not exist".format(name)}, 404
        item.delete_from_db()
        return {"message":"Item was deleted"}


class ItemlistResource(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all() ))}
        # return({'items': [item.json() for item in ItemModel.query.all()]})
