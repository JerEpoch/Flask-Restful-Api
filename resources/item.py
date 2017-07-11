
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price',
			type=float,
			required=True,
			help="This field can't be blank."
		)
	#data = parser.parse_args()

	parser.add_argument('store_id',
		type=int,
		required=True,
		help="Every item needs a store id."
	)

	@jwt_required()
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {"message": "item not found"}, 404
		# item = next(filter(lambda x: x['name'] == name, items), None) # next returns first item found, 
		# # can raise error if no items are found. returns None if not found
		# return {'item': item}, 200 if item else 404




	def post(self,name):
		if ItemModel.find_by_name(name):
			return {'message': "An item with name '{}' already exists.".format(name)}, 400

		data = Item.parser.parse_args()
		
		item = ItemModel(name, **data)
		
		try:
			item.save_to_db()
		except:
			return {"message": "An error occured inserting the item"}, 500 #500 internal server error

		return item.json(), 201



	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()

		return {'message': 'Item deleted'}

	def put(self, name):
		data = Item.parser.parse_args()

		item = ItemModel.find_by_name(name)
		

		if item is None:
			# item = ItemModel(name, data['price'], data['store_id'])
			item = ItemModel(name, **data) # same thing as the above commented code
		else:
			item.price = data['price']

		item.save_to_db()
		return item.json()

		

class ItemList(Resource):
	def get(self):
		return {'items': [item.json() for item in ItemModel.query.all()]}
