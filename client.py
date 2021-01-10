import json
import os.path as path
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


client = Client("Aba", "Shimon", "Abashimon@gmail.com", "052-0000000")
print(client.date_join)
pass
