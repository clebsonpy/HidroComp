class NotStation(Exception):
    def __init__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "FitError: {}".format(self.message) + (" the line {}!".format(self.line) if self.line > 0 else "!")


class FitNotExist(Exception):
    def __init__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "FitNotExist: {}".format(self.message) + (" the line {}!".format(self.line) if self.line > 0 else "!")


class NotStatistic(Exception):
    def __init__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "NotStatistic: {}".format(self.message) + (" the line {}!".format(self.line) if self.line > 0 else "!")


class NotRva(Exception):
    def __init__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "NotRva: {}".format(self.message) + (" the line {}!".format(self.line) if self.line > 0 else "!")


class NotTypePandas(Exception):
    def __init__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "NotRva: {}".format(self.message) + (" the line {}!".format(self.line) if self.line > 0 else "!")


class ObjectError(Exception):
    def __int__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "ObjectErro: {}".format(self.message) + (" the line {}!".format(self.line) if self.line > 0 else "!")


class VariableError(Exception):
    def __int__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "VariableError: {}".format(self.message) + (" the line {}!".format(self.line) if self.line > 0 else "!")


class StatusError(Exception):
    def __int__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "StatusError: {}".format(self.message) + (" the line {}!".format(self.line) if self.line > 0 else "!")