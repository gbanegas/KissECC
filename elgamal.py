
from ecc import EC

class ElGamal(object):
    """ElGamal Encryption
    pub key encryption as replacing (mulmod, powmod) to (ec.add, ec.mul)
    - ec: elliptic curve
    - g: (random) a point on ec
    """
    def __init__(self, ec, g):
        assert isinstance(ec, EC)
        assert ec.is_valid(g)
        self.ec = ec
        self.g = g
        self.n = ec.order(g)
        pass

    def gen(self, priv):
        """generate pub key
        - priv: priv key as (random) int < ec.q
        - returns: pub key as points on ec
        """
        return self.ec.mul(self.g, priv)

    def enc(self, plain, pub, r):
        """encrypt
        - plain: data as a point on ec
        - pub: pub key as points on ec
        - r: random int < ec.q
        - returns: (cipher1, ciper2) as points on ec
        """
        assert self.ec.is_valid(plain)
        assert self.ec.is_valid(pub)
        return (self.ec.mul(self.g, r), self.ec.add(plain, self.ec.mul(pub, r)))

    def dec(self, cipher, priv):
        """decrypt
        - chiper: (chiper1, chiper2) as points on ec
        - priv: private key as int < ec.q
        - returns: plain as a point on ec
        """
        c1, c2 = cipher
        assert self.ec.is_valid(c1) and self.ec.is_valid(c2)
        return self.ec.add(c2, self.ec.neg(self.ec.mul(c1, priv)))
    pass
