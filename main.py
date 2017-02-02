import collections
import math
from ecc import EC
from edwards_curve import EdwardsCurve
from twistedcurves import TwistedEC
from elgamal import ElGamal

Coord = collections.namedtuple("Coord", ["x", "y"])

if __name__ == "__main__":
    # Toy examples
    ec = EC(1, 18, 19)

    ed = EdwardsCurve(ec, 1, 18, 19)
    p1 = Coord(2,1)
    p2 = Coord(1,0)
    p3 = ed.add(p1,p2)
    print p3
    a = -1
    d = float(float(121665)/float(121666))

    p = (2**255)-19

    et = TwistedEC(a, d, p)

    g, _ =  et.at(7)
    eg = ElGamal(et, g)
    # mapping value to ec point
    # "masking": value k to point ec.mul(g, k)
    # ("imbedding" on proper n:use a point of x as 0 <= n*v <= x < n*(v+1) < q)
    mapping = [et.mul(g, i) for i in range(eg.n)]
    print len(mapping)
    plain = mapping[2]
    priv = 5
    pub = eg.gen(priv)
    print plain
    cipher = eg.enc(plain, pub, 15)
    print cipher
    decoded = eg.dec(cipher, priv)
    print decoded
