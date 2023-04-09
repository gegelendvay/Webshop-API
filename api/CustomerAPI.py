from flask import jsonify, request
from flask_restx import Resource, Namespace

from model.Customer import Customer
from model.data import my_shop

CustomerAPI = Namespace('customer', description = 'Customer Management')

@CustomerAPI.route('/')
class GeneralCustomerOps(Resource):
    @CustomerAPI.doc(
        description = "Get a list of all customers."
    )
    def get(self):
        return jsonify(my_shop.customers)

    @CustomerAPI.doc(
        description = "Register a new customer.",
        params = {
            'address': 'Customers address',
            'name': 'Customers name',
            'email': 'Customer Email',
            'dob': 'Customer birthday'
        }
    )
    def post(self):
        args = request.args
        name = args['name']
        email = args['email']
        address = args['address']
        dob = args['dob']
        customer = Customer(name, email, address, dob)
        #return jsonify(customer)
        if my_shop.addCustomer(customer):
            return jsonify(customer)
        else:
            return jsonify("Customer with the email address already exists")

@CustomerAPI.route('/<customer_id>')
class SpecificCustomerOps(Resource):
    @CustomerAPI.doc(
        description = "Get data about a particular customer."
    )
    def get(self, customer_id):
        customer = my_shop.getCustomer(customer_id)
        if not customer:
            return jsonify('Customer ID not found.')
        return jsonify(customer)

    @CustomerAPI.doc(
        description = "Delete an existing customer."
    )
    def delete(self, customer_id):
        customer = my_shop.getCustomer(customer_id)
        if not customer:
            return jsonify('Customer ID not found.')
        my_shop.removeCustomer(customer)
        return jsonify("Customer removed.")

    @CustomerAPI.doc(
        description = "Update customer data.",
        params = {
            'customer_id': 'Customers ID',
            'name': 'Customers name',
            'address': 'Customers address',
            'dob': 'Customer birthday'
        }
    )
    def put(self, customer_id):
        customer = my_shop.getCustomer(customer_id)
        if not customer:
            return jsonify('Customer ID not found.')
        args = request.args
        name = args.get('name', default = customer.name)
        address = args.get('address', default = customer.address)
        dob = args.get('dob', default = customer.dob)
        return jsonify(my_shop.updateCustomer(customer_id, name, address, dob))

@CustomerAPI.route('/verify')
class CustomerVerficiation(Resource):
    @CustomerAPI.doc(
        description = "Verify customer email address",
        params = {
            'token': 'Verification Token sent by email',
            'email': 'Customer Email'
        }
    )
    def put(self):
        args = request.args
        token = args['token']
        email = args['email']
        customer = my_shop.getCustomerbyEmail(email)
        if customer is None:
            return jsonify('Customer ID not found.')
        if customer.verify(token):
            return jsonify('Customer verified.')
        else:
            return jsonify('Invalid token.')
        
@CustomerAPI.route('/<customer_id>/points')
class CustomerPoints(Resource):
    @CustomerAPI.doc(
        description = 'Get the customers bonus points.',
        params = {
            'customer_id': 'Customers ID'
        }
    )
    def get(self, customer_id):
        return jsonify(my_shop.getCustomer(customer_id).bonus_points)
    
    @CustomerAPI.doc(
        description = 'Change customers bonus points.',
        params = {
            'customer_id': 'Customers ID',
            'bonus_points': 'Quantity of bonus points to add'
        }
    )
    def put(self, customer_id):
        args = request.args
        bonus_points = args['bonus_points']
        return jsonify(my_shop.updatePoints(customer_id, bonus_points))

@CustomerAPI.route('/<customer_id>/pwreset')
class CustomerPWReset(Resource):
    @CustomerAPI.doc(
        description = "Generate a temporary password and send via email.",
        params = {
            'customer_id': 'Customers ID'
        }
    )
    def post(self, customer_id):
        customer = my_shop.getCustomer(customer_id)
        if not customer:
            return jsonify('Customer ID not found.')
        return jsonify(customer.generatePass())

    @CustomerAPI.doc(
        description = "Allow password reset based on the temporary password.",
        params = {
            'customer_id': 'Customers ID',
            'temp_pw': 'Password sent by email',
            'new_pw': 'New password'
        }
    )
    def put(self, customer_id):
        args = request.args
        tempPass = args['temp_pw']
        newPass = args['new_pw']
        customer = my_shop.getCustomer(customer_id)
        if not customer:
            return jsonify('Customer ID not found.')
        if customer.resetPass(tempPass, newPass):
            return jsonify('Password changed.')
        else:
            return jsonify('Invalid temporary password. Gerenate a new one.')
        
@CustomerAPI.route('/<customer_id>/add2cart')
class CustomerCart(Resource):
    @CustomerAPI.doc(
        description = 'Add a product to the shopping cart.',
        params = {
            'customer_id': 'Customers ID',
            'product_id': 'Product ID',
            'quantity': 'Quantity of product'
        }
    )
    def put(self, customer_id):
        args = request.args
        product_id = args['product_id']
        quantity = args['quantity']
        return jsonify(my_shop.manageCart(customer_id, product_id, int(quantity)))
        
@CustomerAPI.route('/<customer_id>/order')
class CustomerOrder(Resource):
    @CustomerAPI.doc(
        description = '',
        params = {
            'customer_id': 'Customers ID',
            'shipping_address': 'Shipping address',
            'credit_card': 'Credit card number'
        }
    )
    def post(self, customer_id):
        args = request.args
        shipping_address = args['shipping_address']
        credit_card = args['credit_card']
        return jsonify(my_shop.order(customer_id, shipping_address, credit_card))
        
@CustomerAPI.route('/<customer_id>/orders')
class CustomerOrders(Resource):
    @CustomerAPI.doc(
        description = 'List of previous orders details.',
        params = {
            'customer_id': 'Customers ID'
        }
    )
    def get(self, customer_id):
        return jsonify(my_shop.getOrders(customer_id))
        
@CustomerAPI.route('/<customer_id>/returnable')
class CustomerReturns(Resource):
    @CustomerAPI.doc(
        description = 'List of returnable products.',
        params = {
            'customer_id': 'Customers ID'
        }
    )
    def get(self, customer_id):
        return jsonify(my_shop.returnable(customer_id))
        
@CustomerAPI.route('/<customer_id>/recommendations')
class CustomerRecommendation(Resource):
    @CustomerAPI.doc(
        description = 'Get a list of 10 recommended products.',
        params = {
            'customer_id': 'Customers ID'
        }
    )
    def get(self, customer_id):
        return jsonify(my_shop.recommendProduct(customer_id))