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

    def removeCustomer(self, customer):
        self.customers.remove(customer)

    def updateCustomer(self, customer, name, address, dob): #Move to customer.py
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

    def getCustomer(self, customer):
        for c in self.customers:
            if c.customer_id == customer:
                return c

    def getCustomerbyEmail(self, email):
        for c in self.customers:
            if c.email == email:
                return c

    def addProduct(self, product):
        p = self.getProduct(product.product_id)
        if p == None:
            self.products.append(product)
            return True
        else:
            return False

    def deleteProduct(self, product):
        self.products.remove(product)

    def updateProduct(self, product, quantity):
        p = self.getProduct(product.product_id)
        if p == None:
            self.products.quantity = quantity
            return True
        else:
            return False

    def getProduct(self, prod_id):
        for p in self.products:
            if p.product_id == prod_id:
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
            
    def manageCart(self, customer_id, product_id, quantity):
        customer = self.getCustomer(customer_id)
        if customer:
            product = self.getProduct(product_id)
            if product:
                product.quantity = int(quantity)
                customer.cart.append(product)
                return customer.cart
        return None
            
    def veritfyCard(self, card):
        card = card.replace(" ", "")
        if card.isnumeric() and len(card) == 16:
            return True
        else:
            return False
        
    def order(self, customer_id):
        customer = self.getCustomer(customer_id)
        if customer:
            for i in customer.cart:
                pass
        return False