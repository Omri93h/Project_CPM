from .controller_imports import *


class Controller():
    def __init__(self):
        self.broker = Broker()
        self.view = View()

    def addPortfolio(self):
        newPortData = portfolioForm()
        self.broker.addPortfolio(newPortData)

    def run():
        


    

