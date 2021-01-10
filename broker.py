import json
import os.path as path
from binance.client import Client as binance_client

class Broker:
    """Broker is the main user of CPM """
    def __init__(self):
        """
        Initializing Broker
        """
        
        broker_data = {}
        
        if path.exists("broker_data.json"):
            with open("broker_data.json") as json_file:
                broker_data = json.load(json_file)
            
        if broker_data != {}:
            try:
                self.name = broker_data['name']
                self.API_KEY = broker_data["API_KEY"]
                self.API_SECRET = broker_data["API_SECRET"]
                self.portfolios = broker_data["portfolios"]
                self.binance_client = binance_client(self.API_KEY , self.API_SECRET)
                return
            
            except:
                print("SOMETHING WENT WRONG WITH USER DATA!\nPlease initialize Your Info:")
                
        self.name = input("Name: ") #WILL CHANGED IN VIEW
        self.API_KEY = input("API_KEY: ")
        self.API_SECRET = input("API_SECRET: ")
        self.portfolios = {}
        broker_data = {
            'name': self.name, 
            'API_KEY': self.API_KEY,
            'API_SECRET': self.API_SECRET,
            'portfolios': "",
        }
        
        with open("broker_data.json", 'w') as json_file:
            json.dump(broker_data, json_file)



        
        
        
        
broker = Broker()
pass