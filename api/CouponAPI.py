from flask import jsonify, request
from flask_restx import Resource, Namespace

from model.Coupon import Coupon
from model.data import my_shop

CouponAPI = Namespace('coupons', description = 'Management of coupons')

@CouponAPI.route('/')
class GeneralCouponOps(Resource):
    @CouponAPI.doc(description = 'Get a list of all currently valid coupons.')
    def get(self):
        return jsonify(my_shop.coupons) #Only return valid coupons
    
    @CouponAPI.doc(
        description = '',
        params = {
            'coupon_id': '10 digit coupon ID',
            'category': 'Product category the coupon can be applied to',
            'date': 'Expiry date of the coupon',
            'discount': 'Discount percentage'
        }
    )
    def post(self):
        args = request.args
        coupon_id = args['coupon_id']
        category = args['category']
        date = args['date']
        discount = args['discount']

        newCoupon = Coupon(coupon_id, category, date, discount)
        if my_shop.addCoupon(newCoupon):
            return jsonify(newCoupon)
        else:
            return jsonify('Product with the coupon ID already exists.')