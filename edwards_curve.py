#/bin/python
import collections
from ecc import EC

def inv(x, q):
  return pow(x,q-2,q)

class EdwardsCurve(object):

    def __init__(self, a, d, q):
        EC.__init__(self,a,d,q)
        self.a = a
        self.d = d
        self.q = q
        self.I = I = power_mod(2,(self.q-1)/4,self.q)
        self.zero = [0,1]
        pass

    def edwards(self, P, Q):
        x1 = P[0]
        y1 = P[1]
        x2 = Q[0]
        y2 = Q[1]
        x3 = (x1*y2+x2*y1) * inv(1+d*x1*x2*y1*y2, self.q)
        y3 = (y1*y2+x1*x2) * inv(1-d*x1*x2*y1*y2, self.q)
        return [x3,y3]

    def scalar_multiplication(self, P,e):
        if e == 0: return self.zero
        Q = scalar_multiplication(P,e/2)
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
        factor = self.d*p1[0]*p2[0]*p1[1]*p2[1]
        x = ((p1[0]*p2[1])+(p2[0]*p1[1])/(1 + factor)) % self.q
        y = ((p1[1]*p2[1])-(p2[0]*p1[0])/(1 - factor)) % self.q

        return [x,y]
