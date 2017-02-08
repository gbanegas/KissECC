
class Inverse(object):
    """
    Class to compute the inverse
    """

    @staticmethod
    def inv(x, q):
        return pow(x,q-2,q)
