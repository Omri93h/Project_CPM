
def dashboardView():
    print("Please choose action from theese option :")
    print("1 - view exist portfolio")
    print("2 - add new portfolio")
    print("3 - edit portfolio")
    print("4 - delete portfolio")
    chose = int(input(">>"))
    if chose<1 or chose>4 :
        raise Exception("Incorect chose . Try again .")
    return chose