import collections,sys
from numpy.testing import assert_almost_equal
from utils.inversion import Inverse
from ecc import EC

class TwistedEC(EC):

    def __init__(self, a, b, q, order = None):
        EC.__init__(self, a, b, q)
        """Twisted curve as: (a*x**2 + y**2 = 1 + bx**2y**2) mod q
        - a, b: params of curve formula
        - q: prime number > 2
        """
        assert q > 2 and a <> 0 and b <> 0
        assert a <> b
        assert order <> none
        self.I = pow(2,(self.q-1)/4,self.q)
        self.zero = [0,1]
        self.l = order
        pass

    def is_valid(self, p):
        """
        Verify if the point p is valid in the curve
        """
        x = p[0]
        y = p[1]
        return (-x*x + y*y - 1 - self.b*x*x*y*y) % self.q == 0

    def add(self, p1, p2):
        """ Add two points in the TwistedEC
        """
        p11 = [p1[0], p1[1]]
        p22 = [p2[0], p2[1]]
        if p11 == self.zero: return p22
        if p22 == self.zero: return p11
        factor = self.b*p11[0]*p22[0]*p11[1]*p22[1]
        x = (((p11[0]*p22[1])+(p22[0]*p11[1]))/(1 + factor)) % self.q
        y = (((p11[1]*p22[1])-(self.a*p22[0]*p1[0]))/(1 - factor)) % self.q

        return [x,y]

    def edwards(self, P, Q):
        x1 = P[0]
        y1 = P[1]
        x2 = Q[0]
        y2 = Q[1]
        x3 = (x1*y2+x2*y1) * Inverse().inv(1+self.b*x1*x2*y1*y2, self.q)
        y3 = (y1*y2+x1*x2) * Inverse().inv(1-self.b*x1*x2*y1*y2, self.q)
        return [x3 % self.q,y3 % self.q]

    def scalar_multiplication(self, P,e):
        if e == 0: return self.zero
        Q = self.scalar_multiplication(P,e/2)
        Q = self.edwards(Q,Q)
        if e & 1: Q = self.edwards(Q,P)
        return Q

    def xrecover(self, y):
        xx = (y*y-1) * Inverse().inv(self.b*y*y+1, self.q)
        x = pow(xx,(self.q+3)/8,self.q)
        if (x*x - xx) % self.q != 0: x = (x*self.I) % self.q
        if x % 2 != 0: x = self.q-x
        return x


    def double(self, p):
        """ Double the point p in edwards curve

        """
        assert p <> self.zero
        l1= (self.a*(p[0]**2))
        l2 = (p[1]**2)
        x = float((2*p[0]*p[1])/(l1+l2)) % self.q
        power_y = p[1]**2
        temp = self.a*(p[0]**2)
        y = float((power_y - temp)/(2-l1-l2)) % self.q

        return [x,y]

    def neg(self, p):
        return[-p[0] % self.q, p[1]]
