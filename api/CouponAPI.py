from flask import jsonify, request
from flask_restx import Resource, Namespace

from model.Coupon import Coupon
from model.data import my_shop

CouponAPI = Namespace('coupons', description = 'Management of Coupons')

@CouponAPI.route('/')
class GeneralCouponOps(Resource):
    @CouponAPI.doc(description = 'Get a list of all currently valid coupons.')
    def get(self):
        return jsonify(my_shop.getCoupon())

    @CouponAPI.doc(
        description = 'Add a new coupon.',
        params = {
            'coupon_id': '10 digit coupon ID',
            'category': 'Product category',
            'date': 'Validity date',
            'discount': 'Discount percentage'
        }
    )
    def post(self):
        args = request.args
        coupon_id = args['coupon_id']
        category = args['category']
        date = args['date']
        discount = args['discount']
        coupon = Coupon(coupon_id, category, date, discount)
        #Check if coupon_id is 10 digits long and numeric
        if len(coupon_id) == 10 and coupon_id.isnumeric():
            if my_shop.addCoupon(coupon):
                return jsonify(coupon)
            return jsonify('Coupon ID already exists.')
        return jsonify('Coupon ID is NaN and/or not 10 digits long.')