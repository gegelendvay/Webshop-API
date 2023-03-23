# the instance of shop, where all data is stored.
from model.Customer import Customer
from model.Product import Product
from model.Coupon import Coupon
from model.Shop import Shop

my_shop = Shop()

# Test data
c1 = Customer("Markus Muelle", "markus.mueller@email.test", "1101 Vienna", "10.09.2001")
my_shop.addCustomer(c1)

p1 = Product("Milk", "745GT", "25.03.2023", "Dairy")
my_shop.addProduct(p1)

c1 = Coupon("1234567890", "dairy", "25.03.2024", "0.25")
my_shop.addCoupon(c1)