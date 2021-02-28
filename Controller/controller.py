from .controller_imports import View, Model
from tkinter import *


class Controller():
    def __init__(self):
        # self.root = Tk()
        self.model = Model()
        self.view = View(self)
        # self.dashChoice = {1: self.viewPortfolio,
        #                    2: self.addPortfolio, 6: "exit"}

    def viewPortfolio(self):
        portfolio_id = self.view.choosePortfolioById()
        portFolio = self.model.broker.getPortfoliioByID(portfolio_id)
        self.view.viewPortfolio(portFolio)

    def addPortfolio(self):
        try:
            newPortData = self.view.portfolioForm(
                self.model.broker.Total_Balance)
            self.model.broker.addPortfolio(newPortData)
        except Exception as e:
            print(e)

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
