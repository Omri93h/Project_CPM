from client import Client


class Portfolio(object):
    def __init__(self):
        """
        Initializing Portfolio
        """
        self.start_balance = 0
        self.current_balance = 0
        self.client = None
        self.orders = []
        self.assets = {}
        self.id = -1

    # constructor A
    def New(self, id, start_balance, first_name, last_name, email, phone):
        self.start_balance = start_balance
        self.current_balance = start_balance
        self.client = Client(first_name, last_name, email, phone)
        self.orders = []
        self.assets = {}
        self.id = id
        return self

    # constructor B
    def Exist(self, portfolio):
        self.start_balance = portfolio['start_balance']
        self.current_balance = portfolio['start_balance']
        self.client = Client(portfolio["client"]['first_name'], portfolio["client"]['last_name'],
                             portfolio["client"]['email'], portfolio["client"]['phone'])
        self.orders = portfolio["orders"]
        self.assets = portfolio["assets"]
        self.id = int(portfolio["id"])
        return self

    def getOpenOrders(self):
        open_orders = []
        for order in orders:
            if order['status'] == 'OPEN':
                open_orders.append(order)
        return open_orders

    def getOrdersHistory(self):
        orders_history = []
        for order in orders:
            if order['status'] == 'ClOSED':
                orders_history.append(order)
        return orders_history

    def buyOrder(self, binance_user, base_asset, quote_asset, amount):
        order = binance_user.order_market_buy()


    def addToOrders(self, order_id, status, base_asset, quote_asset, amount):
        order = {"order_id": order_id, "status": status,
                 "base_asset": base_asset, "quote_asset": quote_asset, "amount": amount}
        self.orders.append(order)


