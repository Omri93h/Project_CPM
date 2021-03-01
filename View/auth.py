from time import sleep
from tkinter import *
import json
import os.path as path


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