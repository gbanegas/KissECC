import collections,sys
from numpy.testing import assert_almost_equal
from ecc import EC

def inv(x, q):
  return pow(x,q-2,q)

class TwistedEC(EC):

    def __init__(self, a, b, q):
        EC.__init__(self, a, b, q)
        """Twisted curve as: (a*x**2 + y**2 = 1 + bx**2y**2) mod q
        - a, b: params of curve formula
        - q: prime number > 2
        """
        assert q > 2 and a <> 0 and b <> 0
        assert a <> b
        self.I = pow(2,(self.q-1)/4,self.q)
        self.zero = [0,1]
        pass

    #def power_mod(self, b,e,m):
    #    if e == 0: return 1
    #    t = self.power_mod(b,e/2,m)**2 % m
#        if e & 1: t = (t*b) % m
#        return t


      #return self.power_mod(x,q-2,q)

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

        return [x,y]

    def edwards(self, P, Q):
        x1 = P[0]
        y1 = P[1]
        x2 = Q[0]
        y2 = Q[1]
        x3 = (x1*y2+x2*y1) * inv(1+self.b*x1*x2*y1*y2, self.q)
        y3 = (y1*y2+x1*x2) * inv(1-self.b*x1*x2*y1*y2, self.q)
        return [x3 % self.q,y3 % self.q]

    def scalar_multiplication(self, P,e):
        if e == 0: return self.zero
        Q = self.scalar_multiplication(P,e/2)
        Q = self.edwards(Q,Q)
        if e & 1: Q = self.edwards(Q,P)
        return Q

    def xrecover(self, y):
        xx = (y*y-1) * inv(self.b*y*y+1, self.q)
        x = pow(xx,(self.q+3)/8,self.q)
        if (x*x - xx) % self.q != 0: x = (x*self.I) % self.q
        if x % 2 != 0: x = self.q-x
        return x


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

        return [x,y]

    def neg(self, p):
        return[-p[0] % self.q, p[1]]
