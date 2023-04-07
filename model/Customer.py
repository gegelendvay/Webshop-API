import secrets
import uuid

class Customer:
    def __init__(self, name, email, address, dob):
        self.customer_id = str(uuid.uuid4())
        self.name = name
        self.address = address
        self.email = email
        self.bonus_points = 0
        self.status = "unverified"
        self.verification_token = str(uuid.uuid4())[:5]
        self.dob = dob
        self.password = None
        self.tempPass = None
        self.cart = []
        self.orders = []

    def generatePass(self):
        self.tempPass = secrets.token_urlsafe(16)
        return self.tempPass

    def resetPass(self, tempPass, newPass):
        if self.tempPass == tempPass:
            self.password = newPass
            self.tempPass = None
            return True
        else:
            return False

    def verify(self, token):
        if self.verification_token == token:
            self.status = "verified"
            self.verification_token = None
        return self.status == "verified"