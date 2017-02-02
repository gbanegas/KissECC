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
    a = -1
    d = float(float(121665)/float(121666))

    p = (2**255)-19

    et = TwistedEC(3, 2, 17)

    print et.at(1)
    print et.is_valid(Coord(1,6))
    temp = Coord(1,math.sqrt(2))
    p4 = et.double(Coord(1,math.sqrt(2)))
    p5 = et.add(temp,Coord(1,-math.sqrt(2)))

    print p4
    print p5
    print et.is_valid(p4)
    #print et.mul(Coord(1,6),2)
