class Shop:
    def __init__(self):
        self.customers = []
        self.products = []

    def addCustomer(self, c):
        c1 = self.getCustomerbyEmail(c.email)
        if c1 == None:  # customer does not exist with the given email address
            self.customers.append(c)
            return True
        else:
            return False

    def removeCustomer(self, c):
        self.customers.remove(c)

    def getCustomer(self, cust_id):
        for c in self.customers:
            if c.customer_id == cust_id:
                return c

    def getCustomerbyEmail(self, email):
        for c in self.customers:
            if c.email == email:
                return c

    def addProduct(self, p):
        p1 = self.getProductBySerialNumber(p.serial_number)
        if p1 == None:
            self.products.append(p)
            return True
        else:
            return False
        
    def removeProduct(self, p):
        self.products.remove(p)
        
    def getProduct(self, prod_id):
        for p in self.products:
            if p.product_id == prod_id:
                return p

    def getProductBySerialNumber(self, serial_number):
        for p in self.products:
            if p.serial_number == serial_number:
                return p