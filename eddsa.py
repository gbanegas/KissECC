import hashlib
from twistedcurves import TwistedEC

def H(m):
    return hashlib.sha512(m).digest()

class EdDSA(object):

    def __init__(self, ed):
        """ Creating the EdDSA with a instace of TwistedEC
        """
        assert isinstance(TwistedEC, ed)
