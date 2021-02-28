class Auth:
    def __init__(self):
        self.is_allowed = False

    def Connect(self):
        self.is_allowed = True

    def Disconnect(self):
        self.is_allowed = False

    def isAllowed(self):
        return self.is_allowed
