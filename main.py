import collections
import math
from ecc import EC
from edwards_curve import EdwardsCurve
from twistedcurves import TwistedEC
from eddsa import EdDSA
from elgamal import ElGamal

Coord = collections.namedtuple("Coord", ["x", "y"])


def inv(x, q):
  return power_mod(x,q-2,q)

def power_mod(b,e,m):
    if e == 0: return 1
    t = power_mod(b,e/2,m)**2 % m
    if e & 1: t = (t*b) % m
    return t

if __name__ == "__main__":
    # Toy examples
    a = -1
    q = 2**255 - 19
    d = -121665 * inv(121666, q)
    #l = 2**252 + 27742317777372353535851937790883648493
    print "Strarting...."
    et = TwistedEC(a, d, q)
    edsa = EdDSA(et)
    priv = "gustavo"
    print "Using private key: ", priv
    pubk = edsa.publickey(priv)
    print "Public key generated: ", pubk
    text_to_sign = "Dance Like No One's Watching Encrypt Like Everyone Is"
    print "Signing: ", text_to_sign
    signature, _ = edsa.sign(text_to_sign, priv, pubk)
    print "Signature: ", _
    valid, _ = edsa.validate(signature, text_to_sign, pubk)
    print _
    print "Finished."
