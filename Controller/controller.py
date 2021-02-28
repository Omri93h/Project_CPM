from .controller_imports import *


class Controller():
    def __init__(self):
        self.broker = Broker()
        self.view = View()
        self.dashChoice = {1:self.viewportfolio ,2:self.addPortfolio ,4:self.deletePortfolio ,6:"exit"}
        self.portfolioChoice = {1:self.CreateBuyOrder ,2:self.CreateSellOrder ,3:self.viewCurrentOrders ,7:"exit"}
       
   
    def viewportfolio(self):
        portfolio_id = self.view.choosePortfolioById()
        portFolio = self.broker.getPortfoliioByID(portfolio_id)
        self.view.viewPortfolio(portFolio)      
        choice = self.view.porfolioOptions()
        action = self.portfolioChoice[choice]
        if action == "exit":
            return
        action(portfolio_id)


    def CreateBuyOrder(self,portfolio_id):
        orderDetails = self.view.orderDetails()
        if orderDetails is None :
            return
        orderDetails["action"] = "Buy"
        self.broker.createOrder(portfolio_id,orderDetails)

    def CreateSellOrder(self,portfolio_id):
        orderDetails = self.view.orderDetails()
        if orderDetails is None :
            return
        orderDetails["action"] = "sell"
        self.broker.createOrder(portfolio_id,orderDetails)

    def viewCurrentOrders(self,portfolio_id):
        pass

    def addPortfolio(self):
        try :
            newPortData = self.view.portfolioForm(self.broker.Total_Balance)
            self.broker.addPortfolio(newPortData)
        except Exception as e:
                print(e)  
        else:    
            print("Portfolio was added successfully ")     
      
    def deletePortfolio(self):
        portfolio_id = self.view.choosePortfolioById()
        self.broker.deletePortfolio(portfolio_id)

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


    

