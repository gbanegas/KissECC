#/bin/python
import collections
from ecc import EC

def power_mod(b,e,m):
    if e == 0: return 1
    t = power_mod(b,e/2,m)**2 % m
    if e & 1: t = (t*b) % m
    return t

def inv(x, q):
  return power_mod(x,q-2,q)

Coord = collections.namedtuple("Coord", ["x", "y"])
class EdwardsCurve(object):

    def __init__(self, ec, a, d, q):
        print "Initialized TwistedEC"
        assert isinstance(ec, EC)
        self.a = a
        self.d = d
        self.q = q
        self.I = I = power_mod(2,(self.q-1)/4,self.q)
        self.zero = Coord(0,1)
        pass

    def edwards(self, P, Q):
        x1 = P.x
        y1 = P.y
        x2 = Q.x
        y2 = Q.y
        x3 = (x1*y2+x2*y1) * inv(1+d*x1*x2*y1*y2, self.q)
        y3 = (y1*y2+x1*x2) * inv(1-d*x1*x2*y1*y2, self.q)
        return Coord(x3,y3)

    def scalar_multiplication(self, P,e):
        if e == 0: return self.zero
        Q = scalarmult(P,e/2)
        Q = self.edwards(Q,Q)
        if e & 1: Q = edwards(Q,P)
        return Q

    def xrecover(self, y):
        xx = (y*y-1) * inv(self.d*y*y+1)
        x = power_mod(xx,(q+3)/8,self.q)
        if (x*x - xx) % self.q != 0: x = (x*self.I) % self.q
        if x % 2 != 0: x = self.q-x
        return x


    def add(self, p1, p2):
        if p1 == self.zero: return p2
        if p2 == self.zero: return p1
        factor = self.d*p1.x*p2.x*p1.y*p2.y
        x = ((p1.x*p2.y)+(p2.x*p1.y)/(1 + factor)) % self.q
        y = ((p1.y*p2.y)-(p2.x*p1.x)/(1 - factor)) % self.q

        return Coord(x,y)
