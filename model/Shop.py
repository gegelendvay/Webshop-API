from datetime import date, datetime, timedelta

class Shop:
    def __init__(self):
        #Create empty lists for customers, products and coupons
        self.customers = []
        self.products = []
        self.coupons = []
        #Set the week to the current week
        self.week = datetime.today().isocalendar()[1]

    # Customer functions
    def addCustomer(self, customer):
        if self.getCustomerbyEmail(customer.email) == None:
            self.customers.append(customer)
            return True
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
        #Check if the quantity is valid
        if quantity <= 0 and quantity != -1:
            return 'Invalid quantity'
        if customer:
            product = self.getProduct(product_id)
            if product:
                #Check if we are adding or removing a product from the cart
                if quantity != -1:
                    #Check if there are enough items in the inventory
                    if product.quantity >= quantity:
                        product.cartQuantity = quantity
                        customer.cart.append(product)
                    else:
                        return 'Not enough items in the inventory'
                else:
                    #Check if the product is in the cart
                    if product in customer.cart:
                        customer.cart.remove(product)
                        del product.cartQuantity
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
        if self.getProduct(product.product_id) == None:
            self.products.append(product)
            return True
        return False

    def deleteProduct(self, product):
        self.products.remove(product)

    def updateProduct(self, product, quantity):
        if self.getProduct(product.product_id) == None:
            self.products.quantity = quantity
            return True
        return False

    def getProduct(self, product_id):
        for p in self.products:
            if p.product_id == product_id:
                return p

    # Coupon functions
    def addCoupon(self, coupon):
        if self.getCouponById(coupon.coupon_id) == None:
            self.coupons.append(coupon)
            return True
        return False

    def getCoupon(self):
        coupons = []
        for c in self.coupons:
            #Check if the coupon is still valid
            if datetime.strptime(c.date, "%d.%m.%Y") > datetime.now():
                coupons.append(c)
        return coupons

    def getCouponById(self, coupon):
        for c in self.coupons:
            if c.coupon_id == coupon:
                return c

    # Misc functions
    def veritfyCard(self, credit_card):
        #Remove spaces from the credit card number
        credit_card = credit_card.replace(" ", "")
        #Check if the credit card number is numeric and is 16 digits long
        if credit_card.isnumeric() and len(credit_card) == 16:
            return True
        return False

    def order(self, customer_id, shipping_address, credit_card):
        customer = self.getCustomer(customer_id)
        points, total = 0, 0
        if customer:
            #Verify the credit card number
            validCard = self.veritfyCard(credit_card)
            if validCard:
                if customer.cart:
                    for i in customer.cart:
                        #Calculate the total price and the bonus points
                        points += i.cartQuantity * round(i.price, 0)
                        total += i.cartQuantity * i.price
                        #Get the product and modify its quantity and weekly sale count
                        product = self.getProduct(i.product_id)
                        product.sellProduct(customer_id, i.cartQuantity)
                        #Remove the unnecessary cartQuantity attribute
                        del product.cartQuantity
                    #Calculate the discounted price by using the bonus points
                    #In case the total price would be negative with all the bonus points, set it to 0
                    discounted = max(total - (customer.bonus_points + points) * 0.10, 0)
                    #Update the bonus points
                    self.updatePoints(customer_id, points - round((total - discounted) / 0.10, 0))
                else:
                    return 'Shopping cart is empty.'
            else:
                return 'Invalid credit card number.'
        else:
            return 'Customer ID not found.'
        #Get the date of the order, and add 2 days to it to get the delivery date
        orderDate = date.today().strftime("%d.%m.%Y")
        deliveryDate = (date.today() + timedelta(days = 2)).strftime("%d.%m.%Y")
        #Store the order in the customer's orders list
        customer.orders.append({'orderDate': orderDate, 'deliveryDate': deliveryDate, 'products': customer.cart})
        customer.cart = []
        return 'Your order was succesfully completed!'

    def getReturnable(self, customer_id):
        customer = self.getCustomer(customer_id)
        if not customer:
            return 'Customer ID not found.'
        returnable = []
        for i in customer.orders:
            #If the order was made within the last 14 days, add it to the returnable list
            if datetime.now() - datetime.strptime(i['orderDate'], "%d.%m.%Y") <= timedelta(days = 14):
                returnable.append(i)
        return returnable

    def getRecommended(self, customer_id):
        customer = self.getCustomer(customer_id)
        if not customer:
            return 'Customer ID not found.'
        recommendation = []
        for i in self.products:
            if customer.orders:
                #If the last order's product category is the same as one from the inventory, and there are enough items in the inventory, add it to the recommendation list as long as its length is less than 11
                if i.category == customer.orders[-1]['products'][0].category and i.quantity > 0 and len(recommendation) < 11:
                    recommendation.append(i.name)
        return recommendation

    def getReorders(self):
        #Check if the week has changed
        if self.week != datetime.today().isocalendar()[1]:
            #If it has, reset the weekly sales count for all the products, and update the week number
            for i in self.products:
                i.weeklySales = 0
            self.week = datetime.today().isocalendar()[1]
        reorders = []
        for i in self.products:
            #If the quantity is less than the weekly sales, add it to the reorders list
            if i.quantity < i.weeklySales:
                reorders.append(i)
        return reorders