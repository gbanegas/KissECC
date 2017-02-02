import collections
import math
from ecc import EC
from edwards_curve import EdwardsCurve
from twistedcurves import TwistedEC

Coord = collections.namedtuple("Coord", ["x", "y"])

if __name__ == "__main__":
    # Toy examples
    ec = EC(1, 18, 19)
    ed = EdwardsCurve(ec, 1, 18, 19)
    p1 = Coord(2,1)
    p2 = Coord(1,0)
    p3 = ed.add(p1,p2)
    print p3

    et = TwistedEC(3, 2, 17)
    print et.is_valid(Coord(1,math.sqrt(2)))
