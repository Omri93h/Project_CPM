import datetime


class Client:
    """ Client Info """

    def __init__(self, first_name, last_name, email, phone):
        """
        Initializing Client
        """
        self.date_join = datetime.date.today()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

    def setName(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def setPhone(self, phone_number):
        self.phone = phone_number

    def setEmail(self, email):
        self.email = email
