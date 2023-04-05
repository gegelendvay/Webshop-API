from flask import jsonify, request
from flask_restx import Resource, Namespace

from model.Customer import Customer
from model.Product import Product
from model.data import my_shop

ProductAPI = Namespace('product', description = 'Product Management')

@ProductAPI.route('/')
class AddProduct(Resource):
    @ProductAPI.doc(
        description = 'Add a new product.',
        params = {
            'name': 'Product Name',
            'serial_number': 'Serial Number',
            'expiry': 'Expiry Date',
            'category': 'Product Category'
        }
    )
    def post(self):
        args = request.args
        name = args['name']
        serial_number = args['serial_number']
        expiry = args['expiry']
        category = args['category']

        product = Product(name, serial_number, expiry, category)
        if my_shop.addProduct(product):
            return jsonify(product)
        else:
            return jsonify('Product with the serial number provided already exists.')
    
@ProductAPI.route('/<product_id>')
class ManageProduct(Resource):
    @ProductAPI.doc(
        description = 'Get a product by its ID.'
    )
    def get(self, product_id):
        product = my_shop.getProduct(product_id)
        return jsonify(product)

    @ProductAPI.doc(
        description = 'Delete an existing product.',
        params = {
            'product_id': 'Product ID'
        }
    )
    def delete(self, product_id):
        product = my_shop.getProduct(product_id)
        if not product:
            return jsonify('Product ID {prod_id} was not found')
        my_shop.removeProduct(product)
        return jsonify('Product with ID {prod_id} was removed')

    @ProductAPI.doc(
        description = 'Change the stock of a product.'
    )
    def put(self, product_id):
        pass

@ProductAPI.route('/remove')
class RemoveProduct(Resource):
    @ProductAPI.doc(
        description = 'Remove an item from inventory.',
        params = {
            'product_id': 'Product ID',
            'reason': 'Reason for removal'
        }
    )
    def put(self):
        args = request.args
        product_id = args['product_id']
        reason = args['reason']

        product = my_shop.getProduct(product_id)
        if not product:
            return jsonify('Product ID not found')
        

ProductsAPI = Namespace('products', description = 'Management of Products')

@ProductsAPI.route('/')
class Products(Resource):
    @ProductsAPI.doc(
        description = 'Get a list of all products.'
    )
    def get(self):
        return jsonify(my_shop.products)

@ProductsAPI.route('/reorder')
class Reorder(Resource):
    @ProductsAPI.doc(
        description = 'List products that must be reordered.',
        params = {
            'name': 'Reorder products',
            'expiry': 'expiry date',
            'category': 'product category'
        }
    )
    def get(self):
        pass