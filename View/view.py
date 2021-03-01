from tkinter import *
from .auth import *
from .pages import *


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
