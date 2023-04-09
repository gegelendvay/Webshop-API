import uuid

class Product():
    def __init__(self, name, serial_number, expiry, category):
        self.product_id = str(uuid.uuid4())
        self.name = name
        self.serial_number = serial_number
        self.expiry = expiry
        self.category = category
        self.price = 1
        self.quantity = 1
        self.weeklySales = 0

    def updateStock(self, quantity):
        quantity = int(quantity)
        self.quantity = quantity
        if self.quantity != quantity:
            return True
        return True

    def removeProduct(self):
        self.quantity = 0
        if self.quantity == 0:
            return True
        return False

    def sellProduct(self, customer_id, quantity):
        self.weeklySales += quantity
        self.quantity -= quantity