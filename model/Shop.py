from datetime import date, datetime, timedelta

class Shop:
    def __init__(self):
        self.customers = []
        self.products = []
        self.coupons = []
        self.sold = []

    # Customer functions
    def addCustomer(self, c):
        c1 = self.getCustomerbyEmail(c.email)
        if c1 == None:
            self.customers.append(c)
            return True
        else:
            return False

    def removeCustomer(self, customer):
        self.customers.remove(customer)

    def updateCustomer(self, customer_id, name, address, dob):
        for customer in self.customers:
            if customer.customer_id == customer_id:
                customer.name = name
                customer.address = address
                customer.dob = dob
                return customer
        return False

    def updatePoints(self, customer_id, bonus_points):
        for customer in self.customers:
            if customer.customer_id == customer_id:
                customer.bonus_points += int(bonus_points)
                return customer.bonus_points
        return 'Customer ID not found.'

    def getCustomer(self, customer):
        for c in self.customers:
            if c.customer_id == customer:
                return c

    def getCustomerbyEmail(self, email):
        for c in self.customers:
            if c.email == email:
                return c

    def manageCart(self, customer_id, product_id, quantity):
        customer = self.getCustomer(customer_id)
        #quantity = int(quantity)
        if quantity <= 0 and quantity != -1:
            return 'Invalid quantity count'
        if customer:
            product = self.getProduct(product_id)
            if product:
                if quantity != -1:
                    if product.quantity >= quantity:
                        product.cartQuantity = quantity
                        customer.cart.append(product)
                    else:
                        return 'Not enough items in the inventory'
                else:
                    if product in customer.cart:
                        customer.cart.remove(product)
                    else:
                        return 'Product is not in the cart'
                return customer.cart
        return None

    def getOrders(self, customer_id):
        customer = self.getCustomer(customer_id)
        if not customer:
            return 'Customer ID not found.'
        return customer.orders

    # Product functions
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

    def getProduct(self, product_id):
        for p in self.products:
            if p.product_id == product_id:
                return p

    # Coupon functions
    def addCoupon(self, coupon):
        c = self.getCouponById(coupon.coupon_id)
        if c == None:
            self.coupons.append(coupon)
            return True
        else:
            return False
        
    def getCoupon(self):
        coupons = []
        for c in self.coupons:
            if datetime.strptime(c.date, "%d.%m.%Y") > datetime.now():
                coupons.append(c)
        return coupons

    def getCouponById(self, coupon):
        for c in self.coupons:
            if c.coupon_id == coupon:
                return c
            
    # Misc functions
    def veritfyCard(self, credit_card):
        credit_card = credit_card.replace(" ", "")
        if credit_card.isnumeric() and len(credit_card) == 16:
            return True
        else:
            return False

    def order(self, customer_id, shipping_address, credit_card):
        customer = self.getCustomer(customer_id)
        points, total = 0, 0
        if customer:
            validCard = self.veritfyCard(credit_card)
            if validCard:
                if customer.cart:
                    for i in customer.cart:
                        points += i.cartQuantity * round(i.price, 0)
                        total += i.cartQuantity * i.price
                        product = self.getProduct(i.product_id)
                        product.quantity -= i.quantity
                        del product['cartQuantity']
                        #product.sellProduct(customer_id, i.quantity)
                    total = max(total - (customer.bonus_points + points) * 0.10, 0)
                    self.updatePoints(customer_id, points)
                else:
                    return 'Shopping cart is empty'
            else:
                return 'Invalid credit card'
        else:
            return 'Customer ID not found.'
        orderDate = date.today().strftime("%d.%m.%Y")
        deliveryDate = (date.today() + timedelta(days = 2)).strftime("%d.%m.%Y")
        customer.orders.append({'orderDate': orderDate, 'deliveryDate': deliveryDate, 'products': customer.cart})
        customer.cart = []
        return points, total
        return 'Your order was succesfully completed'

    def returnable(self, customer_id): #Test
        customer = self.getCustomer(customer_id)
        if not customer:
            return 'Customer ID not found.'
        returnable = []
        for i in customer.orders:
            if datetime.now() - datetime.strptime(i['orderDate'], "%d.%m.%Y") <= timedelta(days = 14):
                returnable.append(i)
        return returnable

    def recommendProduct(self, customer_id):
        customer = self.getCustomer(customer_id)
        if not customer:
            return 'Customer ID not found.'
        recommendation = []
        for i in self.products:
            if i.category == customer.orders[-1].products.category:
                recommendation.append(i)
        return recommendation