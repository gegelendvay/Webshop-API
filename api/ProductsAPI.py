from flask import jsonify, request
from flask_restx import Resource, Namespace

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
        return jsonify('Product already exists.')

@ProductAPI.route('/<product_id>')
class ManageProduct(Resource):
    @ProductAPI.doc(
        description = 'Get a product by its ID.'
    )
    def get(self, product_id):
        return jsonify(my_shop.getProduct(product_id))

    @ProductAPI.doc(
        description = 'Delete an existing product.',
        params = {
            'product_id': 'Product ID'
        }
    )
    def delete(self, product_id):
        product = my_shop.getProduct(product_id)
        if not product:
            return jsonify('Product ID not found.')
        my_shop.deleteProduct(product)
        return jsonify('Product removed.')

    @ProductAPI.doc(
        description = 'Change the stock of a product.',
        params = {
            'product_id': 'Product ID',
            'quantity': 'Quantity of the product.'
        }
    )
    def put(self, product_id):
        args = request.args
        quantity = args['quantity']
        product = my_shop.getProduct(product_id)
        if not product:
            return jsonify('Product ID not found.')
        if product.updateStock(quantity):
            return jsonify('Product stock quantity changed.')
        return jsonify('There was an error changing the stock for this product.')

@ProductAPI.route('/sell')
class SellProduct(Resource):
    @ProductAPI.doc(
        description = 'Sell a product.',
        params = {
            'customer_id': 'Customer ID',
            'quantity': 'Quantity to sell'
        }
    )
    def put(self):
        args = request.args
        customer_id = args['customer_args']
        quantity = args['quantity']
        customer = my_shop.getCustomer(customer_id)
        if not customer:
            return 'Customer ID not found.'
        return 'This endpoint cannot be called by itself as it requires a product ID.'

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
            return jsonify('Product ID not found.')
        if product.removeProduct():
            return jsonify(f'Product removed from inventory: {reason}')
        return jsonify('There was an error removing the product')

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
        description = 'List of products that must be reordered.',
    )
    def get(self):
        return jsonify(my_shop.getReorders())