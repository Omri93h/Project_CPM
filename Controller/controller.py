from .controller_imports import *


class Controller():
    def __init__(self):
        self.broker = Broker()
        self.view = View()
        self.dashChoice = {1:self.viewportfolio ,2:self.addPortfolio , 6:"exit"}
        

    def viewportfolio(self):
        portfolio_id = self.view.choosePortfolioById()
        portFolio = self.broker.getPortfoliioByID(portfolio_id)
        self.view.viewPortfolio(portFolio)      


    def addPortfolio(self):
        try :
            newPortData = self.view.portfolioForm(self.broker.Total_Balance)
            self.broker.addPortfolio(newPortData)
        except Exception as e:
                print(e)              
      

    def dashboard(self):
        choice = None
        while choice is None:
            try:           
                choice = self.view.dashboardView()
            except Exception as e:
                print(e)                
        return choice

    def run(self):
        # authorize
        while (1):
            DashChoice = self.dashboard()
            if DashChoice in self.dashChoice :
                runDashChoice = self.dashChoice[DashChoice]
                if runDashChoice == "exit":
                    break                         ## ?return
                runDashChoice()
            else :
                print("This option doesn't exist")


    

