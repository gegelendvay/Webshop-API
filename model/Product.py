import uuid

class Product():
    def __init__(self, name, serial_number, expiry, category):
        self.product_id = str(uuid.uuid4())
        self.name = name
        self.serial_number = serial_number
        self.expiry = expiry
        self.category = category
