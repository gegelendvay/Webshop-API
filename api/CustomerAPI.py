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
        # get the post parameters
        args = request.args
        name = args['name']
        email = args['email']
        address = args['address']
        dob = args['dob']
        newCustomer = Customer(name, email, address, dob)
        # add the customer
        if my_shop.addCustomer(newCustomer):
            return jsonify(newCustomer)
        else:
            return jsonify('Customer with the provided email already exists.')

@CustomerAPI.route('/<customer_id>')
class SpecificCustomerOps(Resource):
    @CustomerAPI.doc(
        description = "Get data about a particular customer."
    )
    def get(self, customer_id):
        customer = my_shop.getCustomer(customer_id)
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
        args = request.args
        name = args['name']
        address = args['address']
        dob = args['dob']
        customer = my_shop.getCustomer(customer_id)
        if not customer:
            return jsonify('Customer ID not found.')
        my_shop.updateCustomer(customer_id, name, address, dob)
        return jsonify('Customer data updated.')


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
        customer = my_shop.getCustomer(customer_id)
        return jsonify(customer.bonus_points)
    
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
        customer = my_shop.getCustomer(customer_id)
        if not customer:
            return jsonify('Customer ID not found.')
        my_shop.updatePoints(customer_id, bonus_points)
        return jsonify('Customer bonus points updated.')

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