import collections
from numpy.testing import assert_almost_equal
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
class TwistedEC(object):

    def __init__(self, a, d, k):
        """Twisted curve as: (a*x**2 + y**2 = 1 + dx**2y**2) mod
        - a, d: params of curve formula
        - k: prime number > 2
        """
        assert k > 2
        assert a <> 0
        assert d <> 0

        self.a = a
        self.d = d
        self.k = k

        self.zero = Coord(0,1)

    def is_valid(self, p):
        """ Verify if a point p is valid in the curve
        """
        assert p <> self.zero
        l = float(self.a*(p.x**2) + (p.y**2)) % self.k
        m = float(1 + (self.d*(p.x**2)*(p.y**2))) % self.k
        print "First: ", l
        print "Second: ", m
        try:
            assert_almost_equal(l, m)
            return True
        except:
            return False


    def add(self, p1, p2):
        if p1 == self.zero: return p2
        if p2 == self.zero: return p1
        factor = self.d*p1.x*p2.x*p1.y*p2.y
        x = ((p1.x*p2.y)+(p2.x*p1.y)/(1 + factor)) % self.k
        y = ((p1.y*p2.y)-(p2.x*p1.x)/(1 - factor)) % self.k

        return Coord(x,y)

    def double(self, p):
        assert p <> self.zero
        factor = self.d*(p.x**2)*(p.y**2)
        x = (2*p.x*p.y)/(1+factor) % self.k
        y = ((p.y**2)-(self.a*(p.x**2)))/(1-factor) % self.k

        return Coord(x,y)

    def neg(self, p):
        return Coord(-p.x % self.k, p.y)
