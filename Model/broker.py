import json
import os.path as path

from binance.client import Client as binance_client

from .portfolio import *


class Broker:
    """Broker is the main user of CPM """

    def __init__(self):
        """
        Initializing Broker
        """

        broker_data = self.loadData()

        if broker_data != {}:
            try:
                self.name = broker_data['name']
                self.API_KEY = broker_data["API_KEY"]
                self.API_SECRET = broker_data["API_SECRET"]
                self.Total_Balance =broker_data["Total_Balance"]
                self.portfolios = []
                self.parsePortfolios(broker_data["portfolios"])
                self.binance_client = binance_client(
                    self.API_KEY, self.API_SECRET)
                return

            except Exception as e:
                print(
                    f"SOMETHING WENT WRONG WITH USER DATA!\n(Error Details: {e}) ")
                print("\n\nPlease initialize Your Info:")

        self.name = input("Name: ")  # WILL CHANGED IN VIEW
        self.API_KEY = input("API_KEY: ")
        self.API_SECRET = input("API_SECRET: ")
        self.Total_Balance = int(input("Total_Balance: "))    ### ###   to change -check the aktual balance 
        self.portfolios = []

        saveData()

    def loadData(self):
        if path.exists("broker_data.json"):
            with open("broker_data.json") as json_file:
                return json.load(json_file)
        else:
            return {}


    def saveData(self):
        broker_data = {
            'name': self.name,
            'API_KEY': self.API_KEY,
            'API_SECRET': self.API_SECRET,
            'Total_Balance':self.Total_Balance
        }
        portfolios = []
        for portfolio in self.portfolios:
            # orders =
            # for i in range(len(self.portfolios.orders)):
            portfolio = {'id': portfolio.id, 'start_balance': portfolio.start_balance,
                         'assets': portfolio.assets, 'orders': portfolio.orders,
                         'client': {'first_name': portfolio.client.first_name,
                                    'last_name': portfolio.client.last_name,
                                    'phone': portfolio.client.phone,
                                    'email': portfolio.client.email
                                    }
                         }
            portfolios.append(portfolio)

        broker_data['portfolios'] = portfolios
        with open("broker_data.json", 'w') as json_file:
            json.dump(broker_data, json_file)

    # creating protfoio objects from list of json  
    def parsePortfolios(self, portfolios):
        for portfolio in portfolios:
            parsed_portfolio = Portfolio().Exist(portfolio)
            self.portfolios.append(parsed_portfolio)

    def deletePortfolio(self, portfolio_id):
        for i in range(len(self.portfolios)):
            if self.portfolios[i].id == portfolio_id:
                del self.portfolios[i]
                self.saveData()
                return
        print(f"Could Not Find Portfolio ID {portfolio_id}")

    def getTotalBalances(self):
        return self.binance_client.get_account()['balances']

    def addPortfolio(self, newPortData):
        id = self.getMaxPortfolioID()
        newPortData["id"] = id
        new_portfolio = Portfolio().New(newPortData)
        self.portfolios.append(new_portfolio)
        self.saveData()

    def getMaxPortfolioID(self):
        if self.portfolios == []:
            return 1  # first portfolio id

        max_id = 1
        for portfolio in self.portfolios:
            if portfolio.id > max_id:
                max_id = portfolio.id
        return max_id + 1

    def getAllTickers(self):
        return self.binance_client.get_all_tickers()

    def getTotalUsdValue(self):
        total = 0
        all_balances = self.getTotalBalances()
        all_tickers = self.getAllTickers()
        for asset in all_balances:
            total_asset_balance = float(asset['free']) + float(asset['locked'])
            for symbol in all_tickers:
                if symbol['symbol'] == asset['asset'] + 'USDT':
                    total += total_asset_balance * float(symbol['price'])
        return total




# broker = Broker()


# order = broker.binance_client.order_market_buy(symbol='IOTABTC',quantity=20)

# print(order)

# broker.deletePortfolio(4)
# pass
