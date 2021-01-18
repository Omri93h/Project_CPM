
def dashboardView():
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