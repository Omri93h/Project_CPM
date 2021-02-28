
class View :
    def __init__(self):
        pass

    def dashboardView(self):
        print("Please choose action from theese option :")
        print("1 - view exist portfolio")
        print("2 - add new portfolio")
        print("3 - edit portfolio")
        print("4 - delete portfolio")
        print("5 - change broker")
        print("6 - exit ")
        choice = int(input(">>"))
        if choice<1 or choice>6 :
            raise Exception("Incorect choice . Try again .")
        return choice
  
    def portfolioForm(self,max_start_balance):
        portfolioData = {}
        print("To add new portfolio  - fill up the new portfolio data please")
        portfolioData["start_balance"] = int(input("start_balance : "))
        if portfolioData["start_balance"] > max_start_balance or portfolioData["start_balance"] <0:
            raise Exception("Invalid start_balance")
        portfolioData["first_name"] = input("first_name : ")
        portfolioData["last_name"] = input("last_name : ")
        portfolioData["email"] = input("email : ")
        portfolioData["phone"] = input("phone : ")
        # to do more validations
        return portfolioData

    def choosePortfolioById(self):
        while 1:
            try:
                portfolio_id = int(input("Portfolio id : "))
            except Exception as e:
                print(e)  
            else:    
                return portfolio_id

    def viewPortfolio(self,portfolioData):
        print(portfolioData)
  

    # def makeMarketOrder(self):
    #     newOrder = {}
    #     print("Make market order ")
    #     orderType = input("Order type (for market buy - 'MB' , for market sell - 'MS'): ")
    #     if orderType != "MB"  or orderType != "MS":
    #         raise Exception("Incorect order type - you should choose ether 'MB' or 'MS'.")
    #     newOrder["Type"] =  orderType
    #     newOrder["symbol"] = input("symbol : ")
    #     newOrder["quantity"] = input("quantity : ") 
    #     ## need validations  ....
    #     return newOrder

    def porfolioOptions(self):
        print("Please choose action from theese option :")
        print("1 - create buy order")
        print("2 - create sell order")
        print("3 - view current orders")
        print("4 - view history orders")
        print("5 - view asses")
        print("6 - edit portfolio details ")
        print("7 - exit ")
        choice = int(input(">>"))
        if choice<1 or choice>7 :
            raise Exception("Incorect choice .")
        return choice


    def orderDetails(self):
        orderDetail = {}
        print("Please set order details :")
        print("For Market ordrer press 'M', for Limit order press 'L' ")
        orderDetail["type"] = input(">>")
        if orderDetail["type"] == "L":
            print("please imput the limit price ")
            orderDetail["price"] = float(input(">>"))
        elif  orderDetail["type"] != "M":
            print ("Incorect choice .")
            return None   
        print("please write the curency pair ")
        orderDetail["symbol"] = input(">>")
        print("please write the require quantity ")
        orderDetail["quantity"] = float(input(">>"))
        return orderDetail        
