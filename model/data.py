# the instance of shop, where all data is stored.
from model.Customer import Customer
from model.Product import Product
from model.Coupon import Coupon
from model.Shop import Shop

my_shop = Shop()

# Test data
customer1 = Customer("Markus Muelle", "markus.mueller@email.test", "1101 Vienna", "10.09.2001")
my_shop.addCustomer(customer1)

product1 = Product("Milk", "745GT", "25.03.2023", "Dairy")
my_shop.addProduct(product1)

product2 = Product("Chicken Thighs", "3446C", "12.04.2023", "Meat")
my_shop.addProduct(product2)

coupon1 = Coupon("1234567890", "dairy", "25.03.2024", "0.25")
my_shop.addCoupon(coupon1)