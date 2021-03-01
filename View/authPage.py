from time import sleep
from tkinter import *
import json
import os.path as path


class EntryWithPlaceholder(Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey70', hide_char=False):
        super().__init__(master)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        self.bind("<FocusIn>", lambda event: self.foc_in(hide_char))
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
    pass  # TO DO ..........


def clickLogin(label_connectionMsg, entry_username, entry_password, controller):
    msg = ""
    fg = "orange"  # Default Error Message

    clickLogin.counter += 1
    label_connectionMsg.configure(text="")

    username = entry_username.get()
    password = entry_password.get()

    if not controller.model.auth.isAllowed():
        if (controller.model.broker.username == username and
                controller.model.broker.password == password):
            msg = "Connected Successfully !"
            fg = "green"
            controller.model.auth.Connect()

        elif clickLogin.counter == 3:
            msg = "Too many Incorrect attempts\nPlease close the program and start it again"
            fg = "red"
        else:
            msg = f'Incorrect Username or Password - Try Again !\n({clickLogin.counter}/3)'

    label_connectionMsg.configure(text=msg, fg=fg)
    label_connectionMsg.pack(pady=10)


# App Configurations
