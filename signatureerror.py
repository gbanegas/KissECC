
class SignatureError(Exception):
    def __init__(self, vef, sig):
        super.__init__(self,"Invalid signature: {0} <> {1} ".format(vef, sig))
        self.vef = vef
        self.sig = sig
