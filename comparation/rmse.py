from comparation.quantify_uncertainty import QuantifyUncertainty


class RMSE(QuantifyUncertainty):

    def __init__(self, reference, compared):
        super().__init__(reference, compared)

    def quantify(self):
        """
        Mean Absolute Percentage Difference
        """
