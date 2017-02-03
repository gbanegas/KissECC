import collections,sys
from numpy.testing import assert_almost_equal
from ecc import EC

Coord = collections.namedtuple("Coord", ["x", "y"])
class TwistedEC(EC):

    def __init__(self, a, b, q):
        EC.__init__(self, a, b, q)
        """Twisted curve as: (a*x**2 + y**2 = 1 + dx**2y**2) mod
        - a, b: params of curve formula
        - q: prime number > 2
        """
        assert q > 2 and a <> 0 and b <> 0
        assert a <> b
        self.zero = Coord(0,1)


    def is_valid(self, p):
        x = p.x
        y = p.y
        return (-x*x + y*y - 1 - self.b*x*x*y*y) % self.q == 0

    def add(self, p1, p2):
        """ Add two points in the TwistedEC
        """
        p11 = Coord(p1[0], p1[1])
        p22 = Coord(p2[0], p2[1])
        if p11 == self.zero: return p22
        if p22 == self.zero: return p11
        factor = self.b*p11.x*p22.x*p11.y*p22.y
        x = (((p11.x*p22.y)+(p22.x*p11.y))/(1 + factor)) % self.q
        y = (((p11.y*p22.y)-(self.a*p22.x*p1.x))/(1 - factor)) % self.q

        return Coord(x,y)

    def double(self, p):
        """ Double the point p in edwards curve

        """
        assert p <> self.zero
        l1= (self.a*(p.x**2))
        l2 = (p.y**2)
        x = float((2*p.x*p.y)/(l1+l2)) % self.q
        power_y = p.y**2
        temp = self.a*(p.x**2)
        y = float((power_y - temp)/(2-l1-l2)) % self.q

        return Coord(x,y)

    def neg(self, p):
        return Coord(-p.x % self.q, p.y)
