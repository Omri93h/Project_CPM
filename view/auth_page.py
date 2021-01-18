from tkinter import *
import json
import os.path as path


class EntryWithPlaceholder(Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey70', hide_char=False):
        super().__init__(master)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        self.bind("<FocusIn>", lambda evernt: self.foc_in(hide_char))
        self.bind("<FocusOut>", self.foc_out)
        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            if args[0] is True:
                self.config(show="*")
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
            self.config(show="")


def getUsernameAndPassword():
    if path.exists("broker_data.json"):
        with open("broker_data.json") as json_file:
            data = json.load(json_file)
            return [data["username"], data["password"]]
    else:
        return {}


def clickRegister(label_registerMsg):
    pass #TO DO ..........


def clickLogin(label_connectionMsg):
    msg = ""
    clickLogin.counter += 1
    label_connectionMsg.configure(text="")

    username = entry_username.get()
    password = entry_password.get()
    auth_data = getUsernameAndPassword()

    if auth_data != {}:
        if auth_data[0] == username and auth_data[1] == password:
            msg = "Connected Successfully !"
            fg = "green"

        elif clickLogin.counter == 3:
            msg = "Too many Incorrect attempts\nPlease close the program and start it again"
            fg = "red"
        else:
            msg = f'Incorrect Username or Password - Try Again !\n({clickLogin.counter}/3)'
            fg = "orange"

    label_connectionMsg.configure(text=msg, fg=fg)
    label_connectionMsg.pack(pady=10)


# App Configurations
window = Tk()
w, h = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry("%dx%d+0+0" % (w*0.8, h*0.9))
window.minsize(600, 300)
background_image = PhotoImage(file="bg.png")
background_label = Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
window.option_add('*font', ('Ubuntu', 13))
window.tk_setPalette(background='white')
window.title('CPM - by David & Omri')

# C = Canvas(TOP, bg="blue", height=250, width=300)
# C.pack()

# Welcome Note
welcome_note = Label(window, text="Welcome to CPM",
                     fg="black", font='Ubuntu 26 bold').pack(pady=(0, 10), fill=X)


# Login
entry_username = EntryWithPlaceholder(window, "Username ...")
entry_username.pack(pady=(100, 10))
entry_username.bind(
    '<Return>', (lambda event: clickLogin(label_connectionMsg)))

entry_password = EntryWithPlaceholder(window, "Password ...", hide_char=True)
entry_password.pack(pady=10)
entry_password.bind(
    '<Return>', (lambda event: clickLogin(label_connectionMsg)))

label_connectionMsg = Label(window, text="")
clickLogin.counter = 0

button_login = Button(window, text="Log In !", font="Ubuntu 16 bold", bg="blue", fg="white",
                      command=lambda: clickLogin(label_connectionMsg))
button_login.pack()

# Create New User

button_createNewUser = Button(window, text="Register !", font="Ubuntu 12 bold",
                              command=lambda: clickRegister(label_registerMsg))
button_createNewUser.pack(pady=(20,30), side=BOTTOM)

frame_register = Frame(window, borderwidth=5, highlightthickness=2)
frame_register.config(highlightbackground="grey")
frame_register.pack(side="bottom")
label_registerMsg = Label(frame_register, text="")

label_or = Label(frame_register, text="or",
                 font=(None, 10)).grid(row=0, column=1)
label_create_new_user = Label(
    frame_register, text="Create a new user:", font='Ubuntu 12 bold').grid(row=1, column=1, pady=(0, 20))

entry_newUsername = EntryWithPlaceholder(frame_register, "New Username ...")
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


window.mainloop()
