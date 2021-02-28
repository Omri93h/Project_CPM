from tkinter import *
import tkinter.ttk as ttk
from .authPage import *
from time import sleep


class View(Tk):
    def __init__(self, controller):
        # Tk.__init__(self)
        self.window = Tk()

        w, h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry("%dx%d+0+0" % (w*0.8, h*0.9))
        self.window.minsize(600, 300)
        self.window.option_add('*font', ('Ubuntu', 13))
        self.window.title('CPM - by David & Omri')
        self.window._frame = None
        self.switchFrame(StartPage, controller)

    def switchFrame(self, frame_class, params=None):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self, params)
        if self.window._frame is not None:
            self.window._frame.destroy()
        self.window._frame = new_frame
        self.window._frame.pack()

    def checkAuth(self, controller):
        if controller.model.auth.isAllowed():
            self.switchFrame(DashboardPage, controller)


class DashboardPage(Frame):
    def __init__(self, master, controller, params=None):
        Frame.__init__(self, master.window)

        label_total_header = Label(self, text="Total Clients Balance:")

        label_total_header.pack(pady=(0, 10), fill=X)
        label_total = Label(self, text=controller.model.broker.total_balance)
        label_total.pack(pady=(0, 10), fill=X)

        label_clients = Label(self, text="My Clients:")
        label_clients.pack(pady=(0, 10), fill=X)

        frame_portfolios = Frame(self, borderwidth=5, highlightthickness=2)
        frame_portfolios.config(highlightbackground="grey")
        frame_portfolios.pack(side="top")

        row_num = 0
        column_num = 0
        portfolios = []
        for portfolio in controller.model.broker.portfolios:
            portfolio_view = Button(
                frame_portfolios, text=portfolio.client.first_name,
                font="Ubuntu 16 bold",
                bg="blue",
                fg="white",
                command=lambda portfolio=portfolio:
                    master.switchFrame(PortfolioPage, [controller, portfolio]))
            portfolios.append(portfolio_view)

        for p in portfolios:
            p.grid(row=row_num, column=column_num)
            if(column_num == 2):
                row_num += 1
                column_num = 0
            else:
                column_num += 1


class StartPage(Frame):
    def __init__(self, master, controller, params=None):
        Frame.__init__(self, master.window)
        # Label(self, text="This is the start page").pack(
        #     side="top", fill="x", pady=10)
        # Button(self, text="Open page one",
        #        command=lambda: master.switchFrame(PageOne)).pack()
        # Button(self, text="Open page two",
        #        command=lambda: master.switchFrame(PageTwo)).pack()

        # auth_page Page Background
        # background_image = PhotoImage(file="bg.png")
        # background_label = Label(self, image=background_image)
        # background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Welcome Note
        welcome_note = Label(self,
                             text="Welcome to CPM",
                             fg="black",
                             font='Ubuntu 26 bold'
                             )
        welcome_note.pack(pady=(0, 10), fill=X)

        # Login
        label_connectionMsg = Label(self, text="")
        clickLogin.counter = 0

        entry_username = EntryWithPlaceholder(self, "Username ...")
        entry_username.pack(pady=(100, 10))
        entry_username.bind(
            '<Return>', (lambda event: clickLogin(
                label_connectionMsg, entry_username, entry_password, controller)))

        entry_password = EntryWithPlaceholder(
            self, "Password ...", hide_char=True)
        entry_password.pack(pady=10)
        entry_password.bind(
            '<Return>', (lambda event: clickLogin(
                label_connectionMsg, entry_username, entry_password, controller)))

        button_login = Button(self, text="Log In !",
                              font="Ubuntu 16 bold",
                              bg="blue",
                              fg="white",
                              command=lambda: [clickLogin(
                                  label_connectionMsg,
                                  entry_username,
                                  entry_password,
                                  controller),
                                  master.checkAuth(controller)])
        button_login.pack()

        # Create New User
        button_createNewUser = Button(self, text="Register !", font="Ubuntu 12 bold",
                                      command=lambda: clickRegister(label_registerMsg))
        button_createNewUser.pack(pady=(20, 30), side=BOTTOM)

        frame_register = Frame(
            self, borderwidth=5, highlightthickness=2)
        frame_register.config(highlightbackground="grey")
        frame_register.pack(side="bottom")
        label_registerMsg = Label(frame_register, text="")

        label_or = Label(frame_register, text="or",
                         font=(None, 10)).grid(row=0, column=1)
        label_create_new_user = Label(
            frame_register, text="Create a new user:", font='Ubuntu 12 bold').grid(row=1, column=1, pady=(0, 20))

        entry_newUsername = EntryWithPlaceholder(
            frame_register, "New Username ...")
        entry_newUsername.grid(row=2, column=0, padx=(50, 0), pady=5)
        entry_newUsername.bind(
            '<Return>', (lambda event: clickRegister(label_registerMsg)))
        entry_nickname = EntryWithPlaceholder(
            frame_register, "Nickname (ex: David) ...")
        entry_nickname.grid(row=3, column=0, padx=(50, 0), pady=5)
        entry_nickname.bind(
            '<Return>', (lambda event: clickRegister(label_registerMsg)))

        entry_newPassword = EntryWithPlaceholder(
            frame_register, "New Password ...", hide_char=True)
        entry_newPassword.grid(row=4, column=0, padx=(50, 0), pady=5)
        entry_newPassword.bind(
            '<Return>', (lambda event: clickRegister(label_registerMsg)))

        entry_ApiKey = EntryWithPlaceholder(
            frame_register, "API Key ...", hide_char=True)
        entry_ApiKey.grid(row=2, column=2, padx=(0, 50), pady=5)
        entry_ApiKey.bind(
            '<Return>', (lambda event: clickRegister(label_registerMsg)))

        entry_ApiSecret = EntryWithPlaceholder(
            frame_register, "API Secret ...", hide_char=True)
        entry_ApiSecret.grid(row=3, column=2, padx=(0, 50), pady=5)
        entry_ApiSecret.bind(
            '<Return>', (lambda event: clickRegister(label_registerMsg)))


class NewOrderPage(Frame):
    def __init__(self, master, params=None):
        Frame.__init__(self, master.window)

        self.price = StringVar(self)
        self.price.set("")

        Label(self, text="Choose Symbol:").pack(
            side="top", fill="x", pady=10)

        style = ttk.Style()
        style.configure('my.TMenubutton', font=('Futura', 20))

        SYMBOLS = [
            "ETH/BTC",
            "BNB/BTC",
            "LTC/BTC"
        ]

        variable = StringVar(self)
        dropdown = ttk.OptionMenu(
            self, variable, SYMBOLS[0], *SYMBOLS, command=self.Callback, style='my.TMenubutton')
        dropdown['menu'].configure(bg="white", font=('futura', 20))
        dropdown.pack(pady=(100, 10))

        Label(self, text="Price:").pack(
            side="top", fill="x", pady=10)

        Label(self, textvariable=self.price).pack(
            side="top", fill="x", pady=10)

        entry_amount = EntryWithPlaceholder(self, "Amount ...")
        entry_amount.pack(pady=(50, 10))
        
        Button(self, text="BUY", bg="green",
               command=lambda:  master.switchFrame(NewOrderPage, params)).pack(pady=(10, 10))
        
        Button(self, text="SELL", bg="red",
               command=lambda:  master.switchFrame(NewOrderPage, params)).pack(pady=(10, 10))

        Button(self, text="Return to Dashboard",
               command=lambda: master.switchFrame(DashboardPage, params[0])).pack(pady=(100, 10))

    def Callback(self, selected):
        print(selected)
        self.price.set("New Price")


class PortfolioPage(Frame):
    def __init__(self, master, params=None):
        Frame.__init__(self, master.window)
        name = params[1].client.first_name + " " + params[1].client.last_name
        Label(self, text=name + " Portfolio:").pack(
            side="top", fill="x", pady=10)

        Button(self, text="New Order",
               command=lambda:  master.switchFrame(NewOrderPage, params)).pack(pady=(100, 10))

        Button(self, text="Return to Dashboard",
               command=lambda: master.switchFrame(DashboardPage, params[0])).pack(side="bottom")


# if __name__ == "__main__":
#     app = View(controller="")
#     app.window.mainloop()
