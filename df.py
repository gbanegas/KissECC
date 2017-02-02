from ecc import EC
class DiffieHellman(object):
    """Elliptic Curve Diffie Hellman (Key Agreement)
    - ec: elliptic curve
    - g: a point on ec
    """
    def __init__(self, ec, g):
        self.ec = ec
        self.g = g
        self.n = ec.order(g)
        pass

    def gen(self, priv):
        """generate pub key"""
        assert 0 < priv and priv < self.n
        return self.ec.mul(self.g, priv)

    def secret(self, priv, pub):
        """calc shared secret key for the pair
        - priv: my private key as int
        - pub: partner pub key as a point on ec
        - returns: shared secret as a point on ec
        """
        assert self.ec.is_valid(pub)
        assert self.ec.mul(pub, self.n) == self.ec.zero
        return self.ec.mul(pub, priv)
    pass
