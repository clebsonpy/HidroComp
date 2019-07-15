

class EstimadorError(Exception):
    def __init__(self, mensagem, linha=0):
        self.mensagem = mensagem
        self.linha = linha

    def __str__(self):
        return "EstimatorError: {}".format(self.mensagem) + \
            (" na linha {}!".format(self.linha) \
            if self.linha > 0 else "!")

class EstimadorNotExist(Exception):
    def __init__(self, mensagem, linha=0):
        self.mensagem = mensagem
        self.linha = linha

    def __str__(self):
        return "EstimatorNotExist: {}".format(self.mensagem) + \
            (" na linha {}!".format(self.linha) \
            if self.linha > 0 else "!")


class AlphaError(Exception):
    def __init__(self, mensagem, linha=0):
        self.mensagem = mensagem
        self.linha = linha

    def __str__(self):
        return "AlphaError: {}".format(self.mensagem) + \
            (" na linha {}!".format(self.linha) \
            if self.linha > 0 else "!")

class ProbabilityError(Exception):
    def __init__(self, mensagem, linha=0):
        self.mensagem = mensagem
        self.linha = linha

    def __str__(self):
        return "ProbabilityError: {}".format(self.mensagem) + \
            (" na linha {}!".format(self.linha) \
            if self.linha > 0 else "!")

class ValueError(Exception):
    def __init__(self, mensagem, linha=0):
        self.mensagem = mensagem
        self.linha = linha

    def __str__(self):
        return "ValueError: {}".format(self.mensagem) + \
            (" na linha {}!".format(self.linha) \
            if self.linha > 0 else "!")

class ValueNotExist(Exception):
    def __init__(self, mensagem, linha=0):
        self.mensagem = mensagem
        self.linha = linha

    def __str__(self):
        return "ValueNotExist: {}".format(self.mensagem) + \
            (" na linha {}!".format(self.linha) \
            if self.linha > 0 else "!")

class DataError(Exception):
    def __init__(self, mensagem, linha=0):
        self.mensagem = mensagem
        self.linha = linha

    def __str__(self):
        return "DataError: {}".format(self.mensagem) + \
            (" na linha {}!".format(self.linha) \
            if self.linha > 0 else "!")

class DataNotExist(Exception):
    def __init__(self, mensagem, linha=0):
        self.mensagem = mensagem
        self.linha = linha

    def __str__(self):
        return "DataNotExist: {}".format(self.mensagem) + \
            (" na linha {}!".format(self.linha) \
            if self.linha > 0 else "!")

class ParameterNotExist(Exception):
    def __init__(self, mensagem, linha=0):
        self.mensagem = mensagem
        self.linha = linha

    def __str__(self):
        return "ParameterNotExist: {}".format(self.mensagem) + \
            (" na linha {}!".format(self.linha) \
            if self.linha > 0 else "!")

class ParameterError(Exception):
    def __init__(self, mensagem, linha=0):
        self.mensagem = mensagem
        self.linha = linha

    def __str__(self):
        return "ParameterError: {}".format(self.mensagem) + \
            (" na linha {}!".format(self.linha) \
            if self.linha > 0 else "!")


class DistributionNotExist(Exception):
    def __init__(self, mensagem, linha=0):
        self.mensagem = mensagem
        self.linha = linha

    def __str__(self):
        return "ParameterError: {}".format(self.mensagem) + \
            (" na linha {}!".format(self.linha) \
            if self.linha > 0 else "!")


class DistributionError(Exception):
    def __init__(self, mensagem, linha=0):
        self.mensagem = mensagem
        self.linha = linha

    def __str__(self):
        return "ParameterError: {}".format(self.mensagem) + \
            (" na linha {}!".format(self.linha) \
            if self.linha > 0 else "!")
