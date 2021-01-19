from .controller_imports import *


class Controller():
    def __init__(self):
        self.broker = Broker()
        self.view = View()
        self.dashChoice = {2:self.addPortfolio}
        

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
        runDashChoice = self.dashChoice[self.dashboard()]
        runDashChoice()



    

