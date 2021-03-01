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
        label_header = Label(self,
                             text="Welcome, " + controller.model.broker.name + "!",
                             fg="black",
                             font='Ubuntu 20 bold'
                             )
        label_header.pack(pady=(0, 20), fill=X)

        label_total_str = Label(
            self, text="Total Clients Balance:", font='Ubuntu 14 bold')
        label_total_str.pack(pady=(20, 10), fill=X)
        label_total_num = Label(
            self, text=str(controller.getTotalBalance()) + "$", font='Ubuntu 26')
        label_total_num.pack(pady=(0, 10), fill=X)

        label_clients = Label(self, text="Clients", font='Ubuntu 14 bold')
        label_clients.pack(pady=(30, 10), fill=X)

        frame_portfolios = Frame(self, borderwidth=5, highlightthickness=2)
        frame_portfolios.config(highlightbackground="grey")
        frame_portfolios.pack(side="top")

        row_num = 0
        column_num = 0
        portfolios = []
        for portfolio in controller.model.broker.portfolios:
            client_name = portfolio.client.first_name + " " + portfolio.client.last_name
            client_value = "{:.2f}".format(
                controller.model.broker.getPorfolioBalance(portfolio.id))
            portfolio_view = Button(
                frame_portfolios, text=client_name +
                "\n\n( " + client_value + "$ )",
                font="Ubuntu 16 bold",
                bg="black",
                fg="white",
                command=lambda portfolio=portfolio:
                    master.switchFrame(PortfolioPage, [controller, portfolio]))
            portfolios.append(portfolio_view)

        for p in portfolios:
            p.grid(row=row_num, column=column_num, padx=20, pady=20)
            if(column_num == 2):
                row_num += 1
                column_num = 0
            else:
                column_num += 1

        Button(self, text="Add Client!", bg="green", fg="white", font='Ubuntu 12 bold',
               command=lambda:
                   master.switchFrame(AddPortfolioPage, controller)).pack(pady=(30, 10))

        Button(self, text="Edit Broker Info", bg="white", fg="black", font='Ubuntu 12',
               command=lambda:
                   master.switchFrame(EditBrokerPage, controller)).pack(pady=(10, 10))


class EditBrokerPage(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master.window)

        self.responseText = StringVar()

        header_frame = Frame(
            self, borderwidth=1, highlightthickness=1)
        header_frame.columnconfigure(0, weight=1)
        header_frame.columnconfigure(1, weight=1)
        header_frame.columnconfigure(2, weight=1)
        header_frame.pack(side="top", fill="both")

        Button(header_frame, text="Back",
               command=lambda: master.switchFrame(DashboardPage, controller)).grid(
                   row=0, column=0, ipadx=30
        )

        label_header = Label(header_frame,
                             text="CLIENT INFO",
                             fg="black",
                             font='Ubuntu 20 bold'
                             )
        label_header.grid(row=0, column=1, ipadx=30)
        Button(header_frame, text="Save", bg="blue", fg="white",
               command=lambda: self.Save(controller)).grid(
                   row=0, column=2, ipadx=30
        )

        broker_data_frame = Frame(
            self, borderwidth=1, highlightthickness=1)
        broker_data_frame.pack(fill="both", pady=50)

        Label(broker_data_frame, text="Binance API KEY: ").grid(row=0, column=0)
        self.entry_API_KEY = Entry(broker_data_frame, width=70)
        self.entry_API_KEY.grid(row=0, column=1)
        self.entry_API_KEY.insert(0, controller.model.broker.API_KEY)

        Label(broker_data_frame, text="Binance API SECRET: ").grid(row=1, column=0)
        self.entry_API_SECRET = Entry(broker_data_frame, width=70)
        self.entry_API_SECRET.grid(row=1, column=1)
        self.entry_API_SECRET.insert(0, controller.model.broker.API_SECRET)

        Label(broker_data_frame, text="Username: ").grid(row=2, column=0)
        self.entry_username = Entry(broker_data_frame, width=70)
        self.entry_username.grid(row=2, column=1)
        self.entry_username.insert(0, controller.model.broker.username)

        Label(broker_data_frame, text="Display Name: ").grid(row=3, column=0)
        self.entry_name = Entry(broker_data_frame, width=70)
        self.entry_name.grid(row=3, column=1)
        self.entry_name.insert(0, controller.model.broker.name)

        Label(broker_data_frame, text="Password: ").grid(row=4, column=0)
        self.entry_password = Entry(broker_data_frame, show="*", width=70)
        self.entry_password.grid(row=4, column=1)
        self.entry_password.insert(0, controller.model.broker.password)

        self.label_response = Label(self, textvariable=self.responseText)
        self.label_response.pack(side=BOTTOM)

        self.label_response = Label(self, textvariable=self.responseText)
        self.label_response.pack(side=BOTTOM)

    def Save(self, controller):
        broker_data = {
            "API_KEY": self.entry_API_KEY.get(),
            "API_SECRET": self.entry_API_SECRET.get(),
            "username": self.entry_username.get(),
            "name": self.entry_name.get(),
            "password": self.entry_password.get()
        }

        response = controller.model.broker.editBroker(broker_data)
        if response:
            self.responseText.set("Youre data has been updated successfully !")
        else:
            self.responseText.set("Something went wrong !")


class EditClientPage(Frame):
    def __init__(self, master, params=None):
        Frame.__init__(self, master.window)
        self.responseText = StringVar()

        header_frame = Frame(
            self, borderwidth=1, highlightthickness=1)
        header_frame.columnconfigure(0, weight=1)
        header_frame.columnconfigure(1, weight=1)
        header_frame.columnconfigure(2, weight=1)
        header_frame.pack(side="top", fill="both")

        Button(header_frame, text="Back",
               command=lambda: master.switchFrame(DashboardPage, params[0])).grid(
                   row=0, column=0, ipadx=30
        )

        label_header = Label(header_frame,
                             text="CLIENT INFO",
                             fg="black",
                             font='Ubuntu 20 bold'
                             )
        label_header.grid(row=0, column=1, ipadx=30)
        Button(header_frame, text="Save", bg="blue", fg="white",
               command=lambda: self.Save(params[0], params[1].id)).grid(
                   row=0, column=2, ipadx=30
        )

        client_data_frame = Frame(
            self, borderwidth=1, highlightthickness=1)
        client_data_frame.pack(fill="both", pady=50)

        Label(client_data_frame, text="First Name:").grid(row=0, column=0)
        self.entry_fname = Entry(client_data_frame)
        self.entry_fname.grid(row=0, column=1)
        self.entry_fname.insert(0, params[1].client.first_name)

        Label(client_data_frame, text="Last Name:").grid(row=1, column=0)
        self.entry_lname = Entry(client_data_frame)
        self.entry_lname.grid(row=1, column=1)
        self.entry_lname.insert(0, params[1].client.last_name)

        Label(client_data_frame, text="Email:").grid(row=2, column=0)
        self.entry_email = Entry(client_data_frame)
        self.entry_email.grid(row=2, column=1)
        self.entry_email.insert(0, params[1].client.email)

        Label(client_data_frame, text="Phone:").grid(row=3, column=0)
        self.entry_phone = Entry(client_data_frame)
        self.entry_phone.grid(row=3, column=1)
        self.entry_phone.insert(0, params[1].client.phone)

        self.label_response = Label(self, textvariable=self.responseText)
        self.label_response.pack(side=BOTTOM)

    def Save(self, controller, portfolio_id):
        client = {
            "first_name": self.entry_fname.get(),
            "last_name": self.entry_lname.get(),
            "email": self.entry_email.get(),
            "phone": self.entry_phone.get()
        }
        response = controller.model.broker.editClient(portfolio_id, client)
        if response:
            self.responseText.set("Client Updated Successfully !")
        else:
            self.responseText.set("Something went wrong !")


class AddPortfolioPage(Frame):
    def __init__(self, master, controller, params=None):
        Frame.__init__(self, master.window)
        self.portfolioData = {
            "start_balance": None,
            "first_name": None,
            "last_name": None,
            "email": None,
            "phone": None,
        }

        self.max_start_balance = 10000
        header_frame = Frame(
            self, borderwidth=1, highlightthickness=1)
        header_frame.pack(side="top", fill="both")

        Button(header_frame, text="Back",
               command=lambda: master.switchFrame(DashboardPage, controller)).grid(
                   row=0, column=0, ipadx=30
        )

        label_header = Label(header_frame,
                             text="Add Portfolio",
                             fg="black",
                             font='Ubuntu 20 bold'
                             )
        label_header.grid(
            row=0, column=1, ipadx=30
        )

        Button(header_frame, text="Add!", bg="blue", fg="white",
               command=lambda: self.Add(entries, master, controller)).grid(
            row=0, column=2, ipadx=30
        )

        entry_start_balance = EntryWithPlaceholder(
            self, "Start Balance in $ ...")
        entry_start_balance.pack(pady=(50, 10))

        entry_first_name = EntryWithPlaceholder(
            self, "Client's first name ...")
        entry_first_name.pack(pady=(10, 10))

        entry_last_name = EntryWithPlaceholder(self, "Client's last name ...")
        entry_last_name.pack(pady=(10, 10))

        entry_phone = EntryWithPlaceholder(self, "Client's Phone name ...")
        entry_phone.pack(pady=(10, 10))

        entry_email = EntryWithPlaceholder(self, "Client's Email ...")
        entry_email.pack(pady=(10, 10))

        entries = [
            entry_start_balance,
            entry_first_name,
            entry_last_name,
            entry_email,
            entry_phone
        ]

        self.responseText = StringVar()
        self.response_label = Label(self, textvariable=self.responseText)
        self.response_label.pack(side=BOTTOM)

    def Add(self, entries, master, controller):
        self.portfolioData["start_balance"] = entries[0].get()
        self.portfolioData["first_name"] = entries[1].get()
        self.portfolioData["last_name"] = entries[2].get()
        self.portfolioData["email"] = entries[3].get()
        self.portfolioData["phone"] = entries[4].get()
        validation = self.Validate()
        if not validation:
            self.responseText.set("Wrong Start Balance")
            return
        response = controller.addPortfolio(self.portfolioData)
        if not response:
            self.responseText.set(
                "You have reached the maximum amount\n of portfolios that you can manage! ")
            return
        self.responseText.set("New Client Added Successfully!")

    def Validate(self):
        # check if data ok
        if (float(self.portfolioData["start_balance"]) > self.max_start_balance or
                float(self.portfolioData["start_balance"]) <= 0):
            raise Exception("Invalid start_balance")
            return False
        return True


class StartPage(Frame):
    def __init__(self, master, controller, params=None):
        Frame.__init__(self, master.window)

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
            '<Return>', (lambda event: [clickLogin(
                label_connectionMsg,
                entry_username,
                entry_password,
                controller),
                master.checkAuth(controller)]))

        entry_password = EntryWithPlaceholder(
            self, "Password ...", hide_char=True)
        entry_password.pack(pady=10)
        entry_password.bind(
            '<Return>', (lambda event: [clickLogin(
                label_connectionMsg,
                entry_username,
                entry_password,
                controller),
                master.checkAuth(controller)]))

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
        button_login.pack(pady=30)

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
        self.selected = StringVar(self)
        self.orderDetails = {
            "type": "M",
            "action": None,
            "quantity": None,
            "symbol": None,
            "price": None
        }

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
        self.selected = SYMBOLS[0]
        dropdown['menu'].configure(bg="white", font=('futura', 20))
        dropdown.pack(pady=(30, 10))

        Label(self, text="Current Price:").pack(
            side="top", fill="x", pady=10)
        Label(self, textvariable=self.price).pack(
            side="top", fill="x", pady=10)

        # Label(frame_order_types, text="Market Order:").grid(
        #     row=0, column=0)
        # Label(frame_order_types, text="Limit Order:").grid(
        #     row=0, column=1)

        # ORDER_TYPES = [
        #     "Market",
        #     "Limit"
        # ]

        # w = Radiobutton(self, "Market")
        # w.pack()

        frame_order_type = Frame(self, borderwidth=5, highlightthickness=2)
        frame_order_type.config(highlightbackground="grey")
        frame_order_type.pack()
        self.order_type = StringVar()
        self.order_type.set("M")

        self.entry_amount = EntryWithPlaceholder(self, "Amount ...")
        self.entry_price = EntryWithPlaceholder(self, "Price ...")
        self.entry_price.config(state="disabled")

        Radiobutton(
            frame_order_type, variable=self.order_type, value="M",
            command=lambda: self.switchOrderType("M")).grid(
            row=0, column=0)
        Label(
            frame_order_type, text="Market").grid(row=0, column=1)
        Radiobutton(
            frame_order_type, variable=self.order_type, value="L", tristatevalue=0,
            command=lambda: self.switchOrderType("L")).grid(
            row=1, column=0)
        Label(
            frame_order_type, text="Limit").grid(row=1, column=1)

        self.entry_amount.pack(pady=(50, 10))
        self.entry_price.pack(pady=(10, 10))

        frame_order_action = Frame(self, borderwidth=0, highlightthickness=0)
        frame_order_action.config(highlightbackground="grey")
        frame_order_action.pack(side="top")

        Button(frame_order_action, text="BUY", bg="green",
               command=lambda:  self.createOrder(params, "Buy")).grid(
            row=0, column=0, padx=20, pady=10)

        Button(frame_order_action, text="SELL", bg="red",
               command=lambda:  self.createOrder(params, "Sell")).grid(
            row=0, column=1, padx=10, pady=10)

        Button(self, text="Return to Dashboard",
               command=lambda: master.switchFrame(DashboardPage, params[0])).pack(pady=(50, 10))

    def Callback(self, selected):
        self.selected = selected
        self.price.set("New Price")

    def switchOrderType(self, order_type):
        self.order_type.set(order_type)
        if order_type == "M":
            self.entry_price.config(state="disabled")
        else:
            self.entry_price.config(state="normal")

    def createOrder(self, params, action):
        self.orderDetails["action"] = action
        self.orderDetails["symbol"] = self.selected.replace("/", "")
        self.orderDetails["quantity"] = self.entry_amount.get()
        self.orderDetails["type"] = self.order_type.get()
        self.orderDetails["price"] = self.entry_price.get()
        params[0].model.broker.createOrder(
            params[1].id, self.orderDetails)


class PortfolioPage(Frame):
    def __init__(self, master, params=None):
        Frame.__init__(self, master.window)
        name = params[1].client.first_name + " " + params[1].client.last_name

        header_frame = Frame(
            self, borderwidth=1, highlightthickness=1)
        header_frame.columnconfigure(0, weight=1)
        header_frame.columnconfigure(1, weight=1)
        header_frame.columnconfigure(2, weight=1)
        header_frame.pack(side="top", fill="both")

        Button(header_frame, text="Back",
               command=lambda: master.switchFrame(DashboardPage, params[0])).grid(
                   row=0, column=0, ipadx=30
        )

        label_header = Label(header_frame,
                             text=name + " Portfolio",
                             fg="black",
                             font='Ubuntu 20 bold'
                             )
        label_header.grid(row=0, column=1, ipadx=30)

        Button(header_frame, text="Delete", fg="white", bg="red",
               command=lambda:  params[0].model.broker.deletePortfolio(params[1].id)).grid(
                   row=0, column=2, ipadx=30
        )

        Label(self,
              text="Assets",
              fg="black",
              font='Ubuntu 14'
              ).pack(pady=(10, 0), fill=X)
        self.assets_frame = Frame(self, borderwidth=1, highlightthickness=1)
        self.insertAssetsData(params[1].assets)

        actions_frame = Frame(
            self, borderwidth=1, highlightthickness=1)
        actions_frame.columnconfigure(0, weight=1)
        actions_frame.columnconfigure(1, weight=1)
        actions_frame.pack(fill=X)
        Button(actions_frame, text="Edit Client Info",
               command=lambda:
                   master.switchFrame(EditClientPage, params)).grid(row=0, column=0, padx=20)
        Button(actions_frame, text="Create New Order", fg="white", bg="blue",
               command=lambda:
                   master.switchFrame(NewOrderPage, params)).grid(row=0, column=1, padx=20)

        Label(self,
              text="Open Orders",
              fg="black",
              font='Ubuntu 14'
              ).pack(pady=(15, 0), fill=X)
        self.frame_open_orders = Frame(
            self, borderwidth=1, highlightthickness=1)
        self.InsertOrdersData("OPEN", params[1].orders, self.frame_open_orders)

        Label(self,
              text="Orders History",
              fg="black",
              font='Ubuntu 14'
              ).pack(pady=(15, 0), fill=X)
        self.frame_orders_history = Frame(
            self, borderwidth=1, highlightthickness=1)
        self.InsertOrdersData(
            "HISTORY", params[1].orders, self.frame_orders_history)

    def insertAssetsData(self, portfolio_assets):
        self.assets_frame.columnconfigure(0, weight=1)
        self.assets_frame.columnconfigure(1, weight=1)
        row = 0
        for asset in portfolio_assets:
            curr_asset = asset[:-3]
            asset_label = Label(self.assets_frame,
                                text=curr_asset)
            asset_label.grid(row=row, column=0, padx=10, pady=2)
            value_label = Label(self.assets_frame,
                                text=portfolio_assets[asset])
            value_label.grid(row=row, column=1, padx=10, pady=2)

            row += 1

        self.assets_frame.pack(pady=(0, 20), fill=X)

    def InsertOrdersData(self, status_flag, portfolio_orders, orders_frame):
        Label(
            orders_frame, text="Symbol").grid(row=0, column=0, padx=50, pady=5)
        Label(
            orders_frame, text="Amount").grid(row=0, column=1, padx=50, pady=5)
        Label(
            orders_frame, text="Status").grid(row=0, column=2, padx=50, pady=5)
        Label(
            orders_frame, text="Order ID").grid(row=0, column=3, padx=50, pady=5)

        row = 1
        for order in portfolio_orders:
            if status_flag == "OPEN":
                adding_condition = (order['status'] == 'NEW')
            else:
                adding_condition = (order['status'] != 'NEW')

            if (adding_condition):
                Label(
                    orders_frame, text=order['symbol']).grid(row=row, column=0, padx=50, pady=2)
                Label(
                    orders_frame, text=order['quantity']).grid(row=row, column=1, padx=50, pady=2)
                Label(
                    orders_frame, text=order['status']).grid(row=row, column=2, padx=50, pady=2)
                Label(
                    orders_frame, text=order['orderId']).grid(row=row, column=3, padx=50, pady=2)
                row += 1

        orders_frame.pack(pady=(0, 20), fill=X)
