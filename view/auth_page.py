from tkinter import *
import json
import os.path as path
from time import sleep


class EntryWithPlaceholder(Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey80', hide_char=False):
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


def getUsernameAndPassword():
    if path.exists("broker_data.json"):
        with open("broker_data.json") as json_file:
            data = json.load(json_file)
            return [data["username"], data["password"]]
    else:
        return {}


def clickExit():
    window.destroy()


def clickConnect(label_connectionMsg):
    msg = ""
    clickConnect.counter += 1
    label_connectionMsg.configure(text="")

    username = entry_username.get()
    password = entry_password.get()
    auth_data = getUsernameAndPassword()

    if auth_data != {}:
        if auth_data[0] == username and auth_data[1] == password:
            msg = "Connected Successfully !"
            fg = "green"

        elif clickConnect.counter == 3:
            msg = "Too many Incorrect attempts\nPlease close the program and start it again"
            fg = "red"
        else:
            msg = f'Incorrect Username or Password - Try Again !\n({clickConnect.counter}/3)'
            fg = "orange"

    label_connectionMsg.configure(text=msg, fg=fg)
    label_connectionMsg.pack()


# App Configurations
window = Tk()
window.wm_attributes('-fullscreen', 1)
window.option_add('*font', ('arial', 16, 'bold'))
window.tk_setPalette(background='white')
window.title('CPM - by David & Omri')


# Exit Button
button = Button(text='QUIT', command=clickExit).pack(anchor='e')


# Welcome Note
welcome_note = Label(window, text="Welcome to CPM", fg="blue", pady=50).pack()


# Username
label_username = Label(window, text="Username: ").pack(pady=10)
entry_username = EntryWithPlaceholder(window, "Username ...")
entry_username.pack()
entry_username.bind(
    '<Return>', (lambda event: clickConnect(label_connectionMsg)))

# Password
label_password = Label(window, text="Password: ").pack(pady=(30, 10))
entry_password = EntryWithPlaceholder(window, "Password ...", hide_char=True)
entry_password.pack()
entry_password.bind(
    '<Return>', (lambda event: clickConnect(label_connectionMsg)))

# Connection
label_connectionMsg = Label(window, text="", pady=20)
clickConnect.counter = 0
button_connect = Button(window, text="Connect !",
                        command=lambda: clickConnect(label_connectionMsg))
button_connect.pack(pady=50)


window.mainloop()
