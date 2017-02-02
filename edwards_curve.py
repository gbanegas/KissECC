#/bin/python
import collections
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

def sqrt_mod(n, q):
    """sqrt on PN modulo: returns two numbers or exception if not exist
    >>> assert (sqrt(n, q)[0] ** 2) % q == n
    >>> assert (sqrt(n, q)[1] ** 2) % q == n
    """
    assert n < q
    for i in range(1, q):
        if i * i % q == n:
            return (i, q - i)
        pass
    raise Exception("not found")

Coord = collections.namedtuple("Coord", ["x", "y"])
class EdwardsCurve(object):

    def __init__(self, ec, a, d, q):
        print "Initialized TwistedEC"
        assert isinstance(ec, EC)
        self.a = a
        self.d = d
        self.q = q

        self.zero = Coord(0,1)
        pass

    def add(self, p1, p2):
        if p1 == self.zero: return p2
        if p2 == self.zero: return p1
        factor = self.d*p1.x*p2.x*p1.y*p2.y
        x = ((p1.x*p2.y)+(p2.x*p1.y)/(1 + factor)) % self.q
        y = ((p1.y*p2.y)-(p2.x*p1.x)/(1 - factor)) % self.q

        return Coord(x,y)
