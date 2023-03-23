class Shop:
    def __init__(self):
        self.customers = []
        self.products = []
        self.coupons = []

    def addCustomer(self, customer):
        c = self.getCustomerbyEmail(customer.email)
        if c == None:
            self.customers.append(customer)
            return True
        else:
            return False
        
    def updateCustomer(self, customer, name, address, dob):
        for c in self.customers:
            if c.customer_id == customer:
                c.name = name
                c.address = address
                c.dob = dob
                return True
            else:
                return False
            
    def updatePoints(self, customer, bonus_points):
        for c in self.customers:
            if c.customer_id == customer:
                c.bonus_points = int(bonus_points)
                return True
            else:
                return False

    def removeCustomer(self, customer):
        self.customers.remove(customer)

    def getCustomer(self, customer):
        for c in self.customers:
            if c.customer_id == customer:
                return c

    def getCustomerbyEmail(self, email):
        for c in self.customers:
            if c.email == email:
                return c

    def addProduct(self, product):
        p = self.getProductBySerialNumber(product.serial_number)
        if p == None:
            self.products.append(product)
            return True
        else:
            return False
        
    def removeProduct(self, product):
        self.products.remove(product)
        
    def getProduct(self, prod_id):
        for p in self.products:
            if p.product_id == prod_id:
                return p

    def getProductBySerialNumber(self, serial_number): #Change to product_id
        for p in self.products:
            if p.serial_number == serial_number:
                return p
            
    def addCoupon(self, coupon):
        c = self.getCouponById(coupon.coupon_id)
        if c == None:
            self.coupons.append(coupon)
            return True
        else:
            return False

    def getCouponById(self, coupon):
        for c in self.coupons:
            if c.coupon_id == coupon:
                return c