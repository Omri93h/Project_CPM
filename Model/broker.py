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
                self.API_KEY = broker_data["API_KEY"]
                self.API_SECRET = broker_data["API_SECRET"]
                self.binance_client = binance_client(
                    self.API_KEY, self.API_SECRET)
                self.name = broker_data['name']
                self.username = broker_data['username']
                self.password = broker_data['password']
                self.total_balance = broker_data["total_balance"]
                self.free_balance = broker_data["free_balance"]
                self.next_portfolio_id = broker_data["next_portfolio_id"]
                self.portfolios = []
                self.parsePortfolios(broker_data["portfolios"])

                return

            except Exception as e:
                print(
                    f"SOMETHING WENT WRONG WITH USER DATA!\n(Error Details: {e}) ")
                print("\n\nPlease initialize Your Info:")

        self.name = input("Name: ")  # WILL CHANGED IN VIEW
        self.API_KEY = input("API_KEY: ")
        self.API_SECRET = input("API_SECRET: ")
        # to change -check the aktual balance
        self.total_balance = int(input("total_balance: "))
        self.free_balance = self.total_balance  # get Total Usd value ??
        self.next_portfolio_id = 0
        self.portfolios = []

        self.saveData()

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
            'total_balance': self.total_balance,
            'free_balance': self.free_balance,
            'next_portfolio_id': self.next_portfolio_id,
            'username': self.username,
            'password': self.password,
        }
        portfolios = []
        for portfolio in self.portfolios:
            # orders =
            # for i in range(len(self.portfolios.orders)):
            portfolio = {'id': portfolio.id, 'start_balance': portfolio.start_balance,
                         "current_balance": portfolio.current_balance,
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
        if(len(self.portfolios) > 6):
            return False
        id = self.next_portfolio_id
        self.next_portfolio_id += 1
        newPortData["id"] = id
        new_portfolio = Portfolio().New(newPortData)
        self.portfolios.append(new_portfolio)
        self.saveData()
        return True

    def saveNewOrder(self, portfolio_id, order):
        orderToSave = {"orderId": order["orderId"], "symbol": order["symbol"],
                       "quantity": order["origQty"], "status": order["status"]}
        for porfolio in self.portfolios:
            if porfolio.id == portfolio_id:
                porfolio.orders.append(orderToSave)
                self.saveData()
                return
        raise Exception("There is no such portfolio id ")

    def getPorfolioBalance(self, portfolio_id):
        total = 0
        for porfolio in self.portfolios:
            if porfolio.id == portfolio_id:
                for symbol, quantity in porfolio.assets.items():
                    symbol = symbol[:-3] + 'USDT'
                    avrPrice = self.binance_client.get_avg_price(symbol=symbol)
                    total += float(quantity) * float(avrPrice["price"])
        return total

    def saveNewAset(self, portfolio_id, asset, action):
        for porfolio in self.portfolios:
            if porfolio.id == portfolio_id:
                if asset["symbol"] in porfolio.assets:
                    if action == "Buy":
                        porfolio.assets[asset["symbol"]
                                        ] += float(asset["amount"])
                    else:
                        porfolio.assets[asset["symbol"]
                                        ] -= float(asset["amount"])
                else:
                    porfolio.assets[asset["symbol"]] = float(asset["amount"])
                self.saveData()
                return
        raise Exception("There is no such portfolio id ")

    def editBroker(self, broker_data):
        self.API_KEY = broker_data["API_KEY"]
        self.API_SECRET = broker_data["API_SECRET"]
        self.name = broker_data["name"]
        self.username = broker_data["username"]
        self.password = broker_data["password"]
        return True

    def editClient(self, portfolio_id, client):
        for portfolio in self.portfolios:
            if portfolio.id == portfolio_id:
                portfolio.client.first_name = client["first_name"]
                portfolio.client.last_name = client["last_name"]
                portfolio.client.phone = client["phone"]
                portfolio.client.email = client["email"]
                self.saveData()
                return True
        raise Exception("There is no such portfolio id ")
        return False

    def updateAllAssets(self):
        for portfolio in self.portfolios:
            for order in portfolio.orders:
                currOrder = self.binance_client.get_order(
                    symbol=order["symbol"], orderId=order['orderId'])
                if order["status"] != currOrder["status"]:
                    order["status"] = currOrder["status"]
                    if currOrder["status"] == 'FILLED':
                        asset = {
                            "symbol": currOrder["symbol"], "amount": currOrder["executedQty"]}
                        if currOrder["side"] == "BUY":
                            action = "Buy"
                        else:
                            action = "Sell"
                        saveNewAset(portfolio.id, asset, action)

    def allowedToSell(self, portfolio_id, orderDetails):
        for porfolio in self.portfolios:
            if porfolio.id == portfolio_id:
                if orderDetails["symbol"] in porfolio.assets:
                    if porfolio.assets[orderDetails["symbol"]] > orderDetails["quantity"]:
                        return True
        return False

    def createOrder(self, portfolio_id, orderDetails):
        self.updateAllAssets()
        try:
            if orderDetails["type"] == "M":
                if orderDetails["action"] == "Buy":
                    order = self.binance_client.order_market_buy(
                        symbol=orderDetails["symbol"], quantity=orderDetails["quantity"])
                else:
                    allow = self.allowedToSell(portfolio_id, orderDetails)
                    if allow == True:
                        order = self.binance_client.order_market_sell(
                            symbol=orderDetails["symbol"], quantity=orderDetails["quantity"])
            else:
                if orderDetails["action"] == "Buy":
                    order = self.binance_client.order_limit_buy(
                        symbol=orderDetails["symbol"], quantity=orderDetails["quantity"], price=orderDetails["price"])
                else:
                    allow = self.allowedToSell(portfolio_id, orderDetails)
                    if allow == True:
                        order = self.binance_client.order_limit_sell(
                            symbol=orderDetails["symbol"], quantity=orderDetails["quantity"], price=orderDetails["price"])
            self.saveNewOrder(portfolio_id, order)
            if order["status"] == "FILLED" or order["status"] == "PARTIALLY_FILLED":
                asset = {"symbol": order["symbol"],
                         "amount": order["executedQty"]}
                self.saveNewAset(portfolio_id, asset, orderDetails["action"])
            print(order)
        except Exception as e:
            print(e)
        return

    def getAllTickers(self):
        return self.binance_client.get_all_tickers()

    def getTotalBalance(self):
        return self.binance_client.get_account()['balances']

    def getTotalUsdValue(self):
        total = 0
        all_balances = self.getTotalBalances()
        all_tickers = self.getAllTickers()
        for asset in all_balances:
            total_asset_balance = float(asset['free']) + float(asset['locked'])
            for symbol in all_tickers:
                if symbol['symbol'] == asset['asset'] + 'USDT':
                    total += total_asset_balance * float(symbol['price'])
        total = "{:.2f}".format(total)
        self.total_balance = total
        self.saveData()
        return total

    def getPortfoliioByID(self, id):
        if self.portfolios == []:
            return None
        for portFolio in self.portfolios:
            if portFolio.id == id:
                return portFolio
        return None

    # def editClientPhone(self,portfolio_id,client_phone):
    #     pass

    # def editClientEmail(self,portfolio_id,client_eemail):
    #     pass

    # def getMaxPortfolioID(self):
    #     if self.portfolios == []:
    #         return 1  # first portfolio id

    #     max_id = 1
    #     for portfolio in self.portfolios:
    #         if portfolio.id > max_id:
    #             max_id = portfolio.id
    #     return max_id + 1

    # def getMaxPortfolioID(self):
    #     if self.portfolios == []:
    #         return 1  # first portfolio id

    #     max_id = 1
    #     for portfolio in self.portfolios:
    #         if portfolio.id > max_id:
    #             max_id = portfolio.id
    #     return max_id + 1

# broker = Broker()


# order = broker.binance_client.order_market_buy(symbol='IOTABTC',quantity=20)

# print(order)

# broker.deletePortfolio(4)
# pass
