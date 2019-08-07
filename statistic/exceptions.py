class FitError(Exception):
    def __init__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "FitError: {}".format(self.message) + \
            (" the line {}!".format(self.line) if self.line > 0 else "!")


class FitNotExist(Exception):
    def __init__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "FitNotExist: {}".format(self.message) + \
               (" the line {}!".format(self.line) if self.line > 0 else "!")


class AlphaError(Exception):
    def __init__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "AlphaError: {}".format(self.message) + \
               (" the line {}!".format(self.line) if self.line > 0 else "!")


class ProbabilityError(Exception):
    def __init__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "ProbabilityError: {}".format(self.message) + \
               (" the line {}!".format(self.line) if self.line > 0 else "!")


class ValueError(Exception):
    def __init__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "ValueError: {}".format(self.message) + \
               (" the line {}!".format(self.line) if self.line > 0 else "!")


class ValueNotExist(Exception):
    def __init__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "ValueNotExist: {}".format(self.message) + \
               (" the line {}!".format(self.line) if self.line > 0 else "!")


class DataError(Exception):
    def __init__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "DataError: {}".format(self.message) + \
               (" the line {}!".format(self.line) if self.line > 0 else "!")


class DataNotExist(Exception):
    def __init__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "DataNotExist: {}".format(self.message) + \
               (" the line {}!".format(self.line) if self.line > 0 else "!")


class ParameterNotExist(Exception):
    def __init__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "ParameterNotExist: {}".format(self.message) + \
               (" the line {}!".format(self.line) if self.line > 0 else "!")


class ParameterError(Exception):
    def __init__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "ParameterError: {}".format(self.message) + \
               (" the line {}!".format(self.line) if self.line > 0 else "!")


class DistributionNotExist(Exception):
    def __init__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "ParameterError: {}".format(self.message) + \
               (" the line {}!".format(self.line) if self.line > 0 else "!")


class DistributionError(Exception):
    def __init__(self, message, line=0):
        self.message = message
        self.line = line

    def __str__(self):
        return "ParameterError: {}".format(self.message) + \
               (" the line {}!".format(self.line) if self.line > 0 else "!")
