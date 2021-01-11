from tkinter import *


def quitApp():
    window.destroy()


def myClick():
    myLabel = Label(window, text=e.get())
    myLabel.pack()


window = Tk()
window.wm_attributes('-fullscreen', 1)
window.option_add('*font', ('arial', 16, 'bold'))

window.title('CPM - by David & Omri')

# Exit Button
button = Button(text='QUIT', command=quitApp).pack()

# Welcome Note
welcome_note = Label(window, text="Welcome to CPM", fg="red", pady=20,).pack()


# Username
label_userName = Label(window, text="Username: ").pack()
userName_entry = Entry(window)
userName_entry.insert(0, "User ...")
userName_entry.pack()

# Password
label_userName = Label(window, text="Password: ", pady=30).pack()
userName_entry = Entry(window)
userName_entry.insert(0, "Password ...")
userName_entry.pack()


myButton = Button(window, text="Connect !", command=myClick,
                  fg="blue", bg="yellow")
myButton.pack()
# myButton.grid()


window.mainloop()
