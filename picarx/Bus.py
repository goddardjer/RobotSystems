class Bus:
    def __init__(self):
        self.message = None

    def write(self, message):
        self.message = message

    def read(self):
        return self.message
