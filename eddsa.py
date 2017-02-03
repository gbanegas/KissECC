import hashlib, collections
from twistedcurves import TwistedEC


Coord = collections.namedtuple("Coord", ["x", "y"])

b = 256
q = 2**255 - 19
l = 2**252 + 27742317777372353535851937790883648493
def hash_function(m):
    return hashlib.sha512(m).digest()

def bit(h,i):
  return (ord(h[i/8]) >> (i%8)) & 1

def inv(x):
  return power_mod(x,q-2,q)

def power_mod(b,e,m):
    if e == 0: return 1
    t = power_mod(b,e/2,m)**2 % m
    if e & 1: t = (t*b) % m
    return t

def xrecover(y):
    xx = (y*y-1) * inv(d*y*y+1)
    x = power_mod(xx,(q+3)/8,q)
    if (x*x - xx) % q != 0: x = (x*I) % q
    if x % 2 != 0: x = q-x
    return x

def edwards(P,Q):
  x1 = P[0]
  y1 = P[1]
  x2 = Q[0]
  y2 = Q[1]
  x3 = (x1*y2+x2*y1) * inv(1+d*x1*x2*y1*y2)
  y3 = (y1*y2+x1*x2) * inv(1-d*x1*x2*y1*y2)
  return [x3 % q,y3 % q]

def scalarmult(P,e):
    if e == 0: return [0,1]
    Q = scalarmult(P,e/2)
    Q = edwards(Q,Q)
    if e & 1: Q = edwards(Q,P)
    return Q

d = -121665 * inv(121666)
By = 4 * inv(5)
Bx = xrecover(By)
B = [Bx % q,By % q]

I = power_mod(2,(q-1)/4,q)
class EdDSA(object):

    def __init__(self, ed):
        """ Creating the EdDSA with a instace of TwistedEC"""
        assert isinstance(ed, TwistedEC)
        self.ed = ed


    def publickey(self, privkey):
        h = hash_function(privkey)
        a = 2**(b-2) + sum(2**i * bit(h,i) for i in range(3,b-2))
        A = scalarmult(B,a)
        return self.encodepoint(A)

    def sign(self, hashval, privkey, pub):
        h = hash_function(privkey)
        a = 2**(b-2) + sum(2**i * bit(h,i) for i in range(3,b-2))
        r = self.__hint__(''.join([h[i] for i in range(b/8,b/4)]) + hashval)
        R = scalarmult(B,r)
        S = (r + self.__hint__(self.encodepoint(R) + pub + hashval) * a) % l
        return self.encodepoint(R) + self.encodeint(S)

    def validate_point(self, p):
        return self.ed.is_valid(p)

    def __hint__(self, m):
        h = hash_function(m)
        return sum(2**i * bit(h,i) for i in range(2*b))

    def __decodeint__(self, s):
        return sum(2**i * bit(s,i) for i in range(0,b))

    def __decodepoint__(self, s):
        y = sum(2**i * bit(s,i) for i in range(0,b-1))
        x = xrecover(y)
        if x & 1 != bit(s,b-1): x = q-x
        P = Coord(x,y)
        if not self.validate_point(P): raise Exception("decoding point that is not on curve")
        return P

    def encodeint(self, y):
        bits = [(y >> i) & 1 for i in range(b)]
        return ''.join([chr(sum([bits[i * 8 + j] << j for j in range(8)])) for i in range(b/8)])

    def encodepoint(self, P):
        x = P[0]
        y = P[1]
        bits = [(y >> i) & 1 for i in range(b - 1)] + [x & 1]
        return ''.join([chr(sum([bits[i * 8 + j] << j for j in range(8)])) for i in range(b/8)])

    def validate(self, signature, message, publickey):
        if len(signature) != b/4: raise Exception("signature length is wrong")
        if len(publickey) != b/8: raise Exception("public-key length is wrong")
        R = self.__decodepoint__(signature[0:b/8])
        A = self.__decodepoint__(publickey)
        S = self.__decodeint__(signature[b/8:b/4])
        h = self.__hint__(self.encodepoint(R) + publickey + message)
        if scalarmult(B,S) != self.ed.add(R,scalarmult(A,h)):
            raise Exception("signature does not pass verification")
