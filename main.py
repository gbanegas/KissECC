import collections
import math
from ecc import EC
from edwards_curve import EdwardsCurve
from twistedcurves import TwistedEC
from eddsa import EdDSA
from elgamal import ElGamal

Coord = collections.namedtuple("Coord", ["x", "y"])

q = 2**255 - 19
def inv(x):
  return power_mod(x,q-2,q)

def power_mod(b,e,m):
    if e == 0: return 1
    t = power_mod(b,e/2,m)**2 % m
    if e & 1: t = (t*b) % m
    return t

if __name__ == "__main__":
    # Toy examples
    a = -1
    d = -121665 * inv(121666)

    l = 2**252 + 27742317777372353535851937790883648493
    et = TwistedEC(a, d, q)

    edsa = EdDSA(et)
    priv = "t"
    pubk = edsa.publickey(priv)
    print "PubKey: ", pubk
    signature = edsa.sign("temp", priv, pubk)

    print "Signature: ", signature

    edsa.validate(signature, "temp", pubk)
