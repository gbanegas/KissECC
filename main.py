import collections
import math
from ecc import EC
from edwards_curve import EdwardsCurve
from twistedcurves import TwistedEC
from elgamal import ElGamal

Coord = collections.namedtuple("Coord", ["x", "y"])

if __name__ == "__main__":
    # Toy examples
    a = -1
    d = float(float(121665)/float(121666))
    p = (2**255)-19
    et = TwistedEC(a, d, p)
