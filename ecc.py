# Basics of Elliptic Curve Cryptography implementation on Python
import collections
from utils.inversion import Inverse
from utils.math_utils import MathUtil

class EC(object):
    """System of Elliptic Curve"""
    def __init__(self, a, b, q):
        """elliptic curve as: (y**2 = x**3 + a * x + b) mod q
        - a, b: params of curve formula
        - q: prime number
        """
        #assert 0 < a and a < q and 0 < b and b < q and q > 2
        #assert (4 * (a ** 3) + 27 * (b ** 2))  % q != 0
        self.a = a
        self.b = b
        self.q = q
        # just as unique ZERO value representation for "add": (not on curve)
        self.zero = [0, 0]
        pass

    def is_valid(self, p):
        if p == self.zero: return True
        l = (p[1] ** 2) % self.q
        r = ((p[0] ** 3) + self.a * p[0] + self.b) % self.q
        return l == r

    def at(self, x):
        """find points on curve at x
        - x: int < q
        - returns: ((x, y), (x,-y)) or not found exception
        >>> a, ma = ec.at(x)
        >>> assert a[0] == ma[0] and a[0] == x
        >>> assert a[0] == ma[0] and a[0] == x
        >>> assert ec.neg(a) == ma
        >>> assert ec.is_valid(a) and ec.is_valid(ma)
        """
        assert x < self.q
        ysq = (x ** 3 + self.a * x + self.b) % self.q
        y, my = MathUtil().sqrt(ysq, self.q)
        return [x, y], [x, my]

    def neg(self, p):
        """negate p
        >>> assert ec.is_valid(ec.neg(p))
        """
        return [p[0], -p[1] % self.q]

    def add(self, p1, p2):
        """<add> of elliptic curve: negate of 3rd cross point of (p1,p2) line
        >>> d = ec.add(a, b)
        >>> assert ec.is_valid(d)
        >>> assert ec.add(d, ec.neg(b)) == a
        >>> assert ec.add(a, ec.neg(a)) == ec.zero
        >>> assert ec.add(a, b) == ec.add(b, a)
        >>> assert ec.add(a, ec.add(b, c)) == ec.add(ec.add(a, b), c)
        """
        if p1 == self.zero: return p2
        if p2 == self.zero: return p1
        if p1[0] == p2[0] and (p1[1] != p2[1] or p1[1] == 0):
            # p1 + -p1 == 0
            return self.zero
        if p1[0] == p2[0]:
            # p1 + p1: use tangent line of p1 as (p1,p1) line
            l = (3 * p1[0] * p1[0] + self.a) * Inverse().inv(2 * p1[1], self.q) % self.q
            pass
        else:
            l = (p2[1] - p1[1]) * Inverse().inv(p2[0] - p1[0], self.q) % self.q
            pass
        x = (l * l - p1[0] - p2[0]) % self.q
        y = (l * (p1[0] - x) - p1[1]) % self.q
        return [x, y]

    def mul(self, p, n):
        """n times <mul> of elliptic curve
        >>> m = ec.mul(p, n)
        >>> assert ec.is_valid(m)
        >>> assert ec.mul(p, 0) == ec.zero
        """
        r = self.zero
        m2 = p
        # O(log2(n)) add
        while 0 < n:
            if n & 1 == 1:
                r = self.add(r, m2)
                pass
            n, m2 = n >> 1, self.add(m2, m2)
            pass
        # [ref] O(n) add
        #for i in range(n):
        #    r = self.add(r, p)
        #    pass
        return r

    def order(self, g):
        """order of point g
        >>> o = ec.order(g)
        >>> assert ec.is_valid(a) and ec.mul(a, o) == ec.zero
        >>> assert o <= ec.q
        """
        assert self.is_valid(g) and g != self.zero
        for i in range(1, self.q + 1):
            if self.mul(g, i) == self.zero:
                return i
            pass
        raise Exception("Invalid order")
    pass
