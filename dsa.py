from ecc import EC

def inv(n, q):
    """div on PN modulo a/b mod q as a * inv(b, q) mod q
    >>> assert n * inv(n, q) % q == 1
    """
    for i in range(q):
        if (n * i) % q == 1:
            return i
        pass
    assert False, "unreached"
    pass

class DSA(object):
    """ECDSA
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

    def sign(self, hashval, priv, r):
        """generate signature
        - hashval: hash value of message as int
        - priv: priv key as int
        - r: random int
        - returns: signature as (int, int)
        """
        assert 0 < r and r < self.n
        m = self.ec.mul(self.g, r)
        return (m.x, inv(r, self.n) * (hashval + m.x * priv) % self.n)

    def validate(self, hashval, sig, pub):
        """validate signature
        - hashval: hash value of message as int
        - sig: signature as (int, int)
        - pub: pub key as a point on ec
        """
        assert self.ec.is_valid(pub)
        assert self.ec.mul(pub, self.n) == self.ec.zero
        w = inv(sig[1], self.n)
        u1, u2 = hashval * w % self.n, sig[0] * w % self.n
        p = self.ec.add(self.ec.mul(self.g, u1), self.ec.mul(pub, u2))
        return p.x % self.n == sig[0]
    pass
