from .client import Client
from .broker import Broker
from .portfolio import Portfolio
from .auth import Auth


class Model:
    def __init__(self):
        self.broker = Broker()
        self.portfolio = Portfolio()
        self.auth = Auth()
