from error import Error
class SignatureError(Error):
    def __init__(self, vef, sig):
        Exception.__init__(self,"Invalid signature: {0} <> {1} ".format(vef, sig))
        self.vef = vef
        self.sig = sig
