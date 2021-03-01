from tkinter import *
from .authPage import *


class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, args[0], **kwargs)

    def show(self):
        self.lift()


class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = Label(self, text="This is page 2")
        label.pack(side="top", fill="both", expand=True)


class PagePortfolio(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = Label(self, text="This is page 3")
        label.pack(side="top", fill="both", expand=True)


class PageDashboard(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label_clients = Label(self, text="My Clients:")
        label_clients.pack(pady=(0, 10), fill=X)

        frame_portfolios = Frame(self, borderwidth=5, highlightthickness=2)
        frame_portfolios.config(highlightbackground="grey")
        frame_portfolios.pack(side="top")
        row_num = 0
        column_num = 0
        portfolios = []
        for portfolio in args[1].model.broker.portfolios:
            portfolio_view = Button(
                frame_portfolios, text=portfolio.client.first_name,
                font="Ubuntu 16 bold",
                bg="blue",
                fg="white",
                command=lambda: portfolioPage)
            portfolio_view.grid(row=row_num, column=column_num)
            if(column_num == 2):
                row_num += 1
                column_num = 0
            else:
                column_num += 1

        # buttonframe = Frame(self)
        # buttonframe.pack(side="top", fill="x", expand=False)
        # b3 = Button(buttonframe, text="Page 3", command=args[2].lift)
        # b3.pack(side="left")


class PageAuth(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

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
                label_connectionMsg, entry_username, entry_password, args[1], args[2])))

        entry_password = EntryWithPlaceholder(
            self, "Password ...", hide_char=True)
        entry_password.pack(pady=10)
        entry_password.bind(
            '<Return>', (lambda event: clickLogin(
                label_connectionMsg, entry_username, entry_password, args[1], args[2])))

        button_login = Button(self, text="Log In !",
                              font="Ubuntu 16 bold",
                              bg="blue",
                              fg="white",
                              command=lambda: clickLogin(
                                  label_connectionMsg,
                                  entry_username,
                                  entry_password,
                                  args[1], args[2]))
        button_login.pack()

        # Create New User
        button_createNewUser = Button(self, text="Register !", font="Ubuntu 12 bold",
                                      command=lambda: clickRegister(label_registerMsg))
        button_createNewUser.pack(pady=(20, 30), side=BOTTOM)

        frame_register = Frame(self, borderwidth=5, highlightthickness=2)
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


class MainView(Frame):
    def __init__(self, controller):
        Frame.__init__(self)
        container = Frame(self)

        portfolio_page = PagePortfolio(self)
        dashboard_page = PageDashboard(self, controller, portfolio_page)
        auth_page = PageAuth(self, controller, dashboard_page)

        auth_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        dashboard_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        portfolio_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        container.pack(side="top", fill="both", expand=True)
        auth_page.show()


class View(Frame):
    def __init__(self, controller):  # window as "master"
        w, h = controller.root.winfo_screenwidth(), controller.root.winfo_screenheight()
        controller.root.geometry("%dx%d+0+0" % (w*0.8, h*0.9))
        controller.root.minsize(600, 300)
        controller.root.option_add('*font', ('Ubuntu', 13))
        controller.root.title('CPM - by David & Omri')

        main = MainView(controller)
        main.pack(side="top", fill="both", expand=True)
