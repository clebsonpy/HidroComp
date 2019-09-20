class Flow(Exception):
    def __init__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "FitError: {}".format(self.message) + (" the line {}!".format(self.line) if self.line > 0 else "!")
