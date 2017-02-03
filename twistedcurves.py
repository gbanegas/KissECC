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
        self.zero = Coord(0,1)


    def add(self, p1, p2):
        """ Add two points in the TwistedEC
        """
        if p1 == self.zero: return p2
        if p2 == self.zero: return p1
        factor = self.d*p1.x*p2.x*p1.y*p2.y
        x = (((p1.x*p2.y)+(p2.x*p1.y))/(1 + factor)) % self.q
        y = (((p1.y*p2.y)-(self.a*p2.x*p1.x))/(1 - factor)) % self.q

        return Coord(x,y)

    def double(self, p):
        """ Double the point p.

        """
        assert p <> self.zero
        #factor = self.d*(p.x**2)*(p.y**2)
        l1= (self.a*(p.x**2))
        l2 = (p.y**2)
        x = float((2*p.x*p.y)/(l1+l2)) % self.q
        power_y = p.y**2
        temp = self.a*(p.x**2)
        y = float((power_y - temp)/(2-l1-l2)) % self.q

        return Coord(x,y)

    def neg(self, p):
        return Coord(-p.x % self.q, p.y)
