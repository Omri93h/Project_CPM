from .controller_imports import View, Model
from tkinter import *


class Controller():
    def __init__(self):
        self.model = Model()
        self.view = View(self)

    def viewPortfolio(self):
        portfolio_id = self.view.choosePortfolioById()
        portFolio = self.model.broker.getPortfoliioByID(portfolio_id)
        self.view.viewPortfolio(portFolio)

    def addPortfolio(self, portfolio):
        res = self.model.broker.addPortfolio(portfolio)
        return res

    def getTotalBalance(self):
        return self.model.broker.getTotalUsdValue()

    def Dashboard(self):
        choice = None
        while choice is None:
            try:
                choice = self.view.dashboardView()
            except Exception as e:
                print(e)
        return choice

    def run(self):
        self.view.window.deiconify()
        self.view.window.mainloop()

        # authorize
        # while (1):
        #     DashChoice = self.Dashboard()
        #     if DashChoice in self.dashChoice:
        #         runDashChoice = self.dashChoice[DashChoice]
        #         if runDashChoice == "exit":
        #             break  # ?return
        #         runDashChoice()
        #     else:
        #         print("This option doesn't exist")
